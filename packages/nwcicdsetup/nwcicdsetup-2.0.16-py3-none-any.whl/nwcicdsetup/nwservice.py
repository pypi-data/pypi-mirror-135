import asyncio
import json
import os
import re
from enum import Enum, unique
from pathlib import Path
from typing import Any, Coroutine, Dict, List, Optional, Set, Tuple, Union

import yaml
from schema import SchemaError

from nwcicdsetup.circleci import check_change_async, check_dotnet_change_async
from nwcicdsetup.circlecicontext import CircleCIContext
from nwcicdsetup.validationschema import approval_task_name, service_validate


@unique
class Context(Enum):
    FEATURE = 0
    DEV = 1
    TEST = 2
    STAGE = 3
    PRODUCTION = 4


class NWServiceContext:
    """Giving overall information this generation is running on"""

    def __init__(
            self,
            circleci_context: CircleCIContext,
            services: Dict[str, "NWService"],
            general_config: Dict[str, Any],
            cwd: str,
            global_dependencies: List[str] = [],
            fake_deploy: bool = False,
            force: bool = False):

        self.cwd = cwd.replace("\\", "/")
        """current working directory"""
        self.fake_deploy: bool = fake_deploy
        """replace deploy logic with an echo"""
        self.force: bool = force
        """indicating to force run of all tasks"""
        self.global_dependencies = list(global_dependencies)
        """dependencies which cause a global rebuild"""
        self.services: Dict[str, NWService] = services
        """all services mapped via their ids"""
        self.circleci_context = circleci_context
        """we write this ref here on purpose so we see changes from the outside class internally"""

        self.general_config: Dict[str, Dict[str, Any]] = dict(general_config)
        """key/value pairs containing all general and cicd commands, executors that tasks can use to run"""

    @property
    def branch(self) -> str:
        """returns the name of the current branch this is running on"""
        return self.circleci_context.branch

    @property
    def job_context(self) -> Context:
        return NWServiceContext.branch_to_context(self.branch)

    @staticmethod
    def branch_to_context(branch: str) -> Context:
        branch = branch.lower()
        if branch == "develop":
            return Context.DEV
        elif branch == "testing":
            return Context.TEST
        elif branch == "staging":
            return Context.STAGE
        elif branch == "master" or branch == "main":
            return Context.PRODUCTION

        return Context.FEATURE


class NWApproval:
    """Encapsulation resulting in an Circleci approval workflow step"""

    def __init__(self, service: "NWService", id: str, members: Dict[str, Any]):
        self.id = id
        self.service = service
        self.name = f"{service.name}-{id}-approve-job"
        self.requires: List[str] = list(members["requires"])
        """wait for completion on this approval job"""

    def to_yaml(self) -> Dict[str, Any]:
        return {
            self.name: {
                "type": "approval",
                "requires": self.service.job_names_for_requires_references(self.requires)
            }
        }


class NWService:
    """Encapsulation of the cicd.yml files which is processing task data"""

    def __init__(self, context: "NWServiceContext", config_path: str):
        self.approvals: Dict[str, NWApproval] = {}
        """all parsed approval jobs resulting in Circleci workflow approvals"""
        self.context: NWServiceContext = context
        """context information"""
        self.name: str = ""
        """name of the parsed cicd.yml - assigned from its 'name' atttribute"""
        self.layers: List[Set[str]] = []
        """tasks names per layer"""
        self.tasks: Dict[str, NWTask] = {}
        """parsed 'tasks' section of the cicd.yml mainly controlling the building part"""
        self.path = os.path.dirname(config_path).replace(
            "\\\\", "/").replace("\\", "/")
        """path to the cicd.yml file relative from the root"""

        try:
            print(f"process config '{config_path}'")

            with open(config_path, mode="rb") as config_stream:
                loaded_config = yaml.safe_load(json.dumps(json.loads(config_stream.read()))
                                               ) if ".json" in config_path else yaml.safe_load(config_stream)
            nodes = service_validate(loaded_config, context.general_config)

            self.name = nodes["name"]
            # build up build layers containing task ids which can be used to resolve
            # tasks of self.tasks dictionary
            for layer in nodes["layers"]:
                tasks: Set[str] = set()
                self.layers.append(tasks)
                for layer_tasks in layer.values():
                    for task_name, task in layer_tasks.items():
                        tasks.add(task_name)
                        if approval_task_name.match(task_name):
                            self.approvals |= {
                                task_name: NWApproval(service=self,
                                                      id=task_name,
                                                      members=task)
                            }
                        else:
                            self.tasks |= {
                                task_name: NWTask(name=task_name,
                                                  service=self,
                                                  members=task)
                            }

            # setup requires depending on layers
            for task in [*self.tasks.values(), *self.approvals.values()]:
                task.requires += self.get_preceding_layers_references_for(
                    task.id)
                task.requires = list(set(task.requires))
                task.requires.sort()

        except SchemaError as e:
            print(f"Error when processing {config_path}")
            raise e

    @property
    def context_name(self) -> str:
        c = self.context.job_context
        context_prefix = os.environ.get("CIRCLE_CONTEXT_PREFIX")
        context_prefix = context_prefix if context_prefix else ""

        if c == Context.FEATURE:
            return f"{context_prefix}feature"
        if c == Context.DEV:
            return f"{context_prefix}dev"
        if c == Context.TEST:
            return f"{context_prefix}test"
        if c == Context.STAGE:
            return f"{context_prefix}stage"
        if c == Context.PRODUCTION:
            return f"{context_prefix}prod"

        raise Exception(f"Cant find context for {self.name}")

    @property
    def all_jobs(self) -> Dict[str, Union["NWTask", "NWApproval"]]:
        """returns a dictionary containing all jobs or this service"""
        return self.tasks | self.approvals

    def get_preceding_layers_references_for(self, id: str) -> List[str]:
        """returns all task ids of preceding layers for the given task or approval id"""
        depending: List[str] = []

        # collect tasks until we find the containing layer
        for layer_tasks in self.layers:
            if id in layer_tasks:
                break
            for task_id in layer_tasks:
                if task_id in self.tasks:
                    depending.append(f"{self.name}:{self.tasks[task_id].id}")
                else:
                    depending.append(
                        f"{self.name}:{self.approvals[task_id].id}")

        return depending

    def job_names_for_requires_references(self, requires: List[str]) -> List[str]:
        """List of job names for all given requires references"""
        required: List[str] = []
        for id in requires:
            service_id, job_id = id.split(":")

            # link all jobs from the service?
            requires_all = bool(re.search("[\\*]+", job_id))
            # validate the service and the tasks to find
            if not service_id in self.context.services:
                raise Exception(f"Nothing found for {service_id} in '{id}'")
            required_service = self.context.services[service_id]

            all_jobs = required_service.all_jobs
            if not job_id in all_jobs and not requires_all:
                raise Exception(f"Nothing found for {job_id} in '{id}'")

            if requires_all:
                required += [j.name for j in all_jobs.values()]
            else:
                required.append(all_jobs[job_id].name)
        return required

    async def check_changes_for_required(self, requires: List[str]) -> Tuple[bool, Dict[str, Any]]:
        """retrieves change status of tasks via dependency_ids"""

        services = self.context.services

        def tasks_for(reference: str) -> List[Coroutine[Any, Any, bool]]:
            service_id, job_id = reference.split(":")

            # link all jobs from the service?
            requires_all = bool(
                re.search('[\\*]+', job_id))

            # validate the service and the tasks to find
            if not service_id in services:
                raise Exception(
                    f"No service found for {service_id} in '{reference}'")

            service = services[service_id]
            if not job_id in service.tasks and not requires_all:
                raise Exception(
                    f"No task-reference found for {job_id} in '{reference}'")

            tasks = [t.is_changed_async for t in service.tasks.values()] if requires_all else [
                service.tasks[job_id].is_changed_async]
            return tasks

        async def to_result(t: Coroutine[Any, Any, bool], reference: str) -> Tuple[bool, Dict[str, Any]]:
            return (await t, {"required task": reference})

        def is_approval(reference: str) -> bool:
            service_id, id = reference.split(":")
            if not service_id in services:
                raise Exception(
                    f"No service found for {service_id} in '{reference}'")
            return id in services[service_id].approvals

        requires = list(filter(lambda x: not is_approval(x), requires)
                        )

        tasks = [to_result(t, reference)
                 for reference in requires for t in tasks_for(reference)]
        results = list(await asyncio.gather(*tasks))
        changed = any(filter(lambda x: x[0], results))

        if changed:
            info: Dict[str, Any] = {}
            for result in results:
                info |= result[1]
            return (True, info)
        return (False, {})

    async def job_yaml_async(self) -> Dict[str, Any]:
        """returns all task in form of a yml compliant dictionary"""
        print(f"Generate jobs for service '{self.name}'")

        tasks = [task.task_to_yaml_async() for task in self.tasks.values()]
        jobs: Dict[str, Any] = {}
        for a in await asyncio.gather(*tasks):
            jobs |= a

        return jobs

    async def workflow_jobs_async(self) -> List[Dict[str, Any]]:
        # enable yml dumper caching via aliases
        if not "yml_branch_filter" in globals():
            g = globals()
            g["yml_branch_filter"] = {
                "branches": {"only": self.context.branch}}
        yml_branch_filter = (globals())["yml_branch_filter"]

        def workflow_job(dependency_ids: List[str], name: str, custom_dependencies: List[str] = []) -> Dict[str, Any]:
            yml_obj = {
                "context": self.context_name,
                "filters": yml_branch_filter
            }
            required = self.job_names_for_requires_references(
                dependency_ids)
            if len(required) > 0:
                yml_obj["requires"] = required + custom_dependencies
            return {name: yml_obj}

        # workflow jobs for tasks:
        jobs: List[Dict[str, Any]] = []
        for task in self.tasks.values():
            jobs.append(workflow_job(task.requires, task.name))

        # workflow jobs for approvals:
        for approval in self.approvals.values():
            jobs.append(approval.to_yaml())

        return jobs


class NWTask:

    def __init__(self, name: str, service: "NWService", members: Dict[str, Any]):
        self._is_changed: Optional[bool] = None
        """private flag caching a previous call to is_changed_async()"""
        self._lock = asyncio.Lock()
        """the lock used for is_changed_async()"""
        self.change_info: Dict[str, Any] = {}
        """changeset information available after first call to is_changed_async()"""
        self.commands: List[Dict[str, Dict[str, Union[str, float, bool]]]] = list(
            members["commands"])
        """command and parameters this task will be linked to"""
        self.dependencies: List[str] = list(members["dependencies"])
        """dependencies that will considered to determine changeset and trigger the job"""
        self.executor: str = members["executor"]
        """executor to be used for the generated job"""
        self.path: str = os.path.normpath(os.path.join(service.path, members["path"])
                                          ).replace("\\", "/")
        """path of this task relative from cicd.yml"""
        self.resource_class: str = members["resource_class"]
        """the resource class used for job generation"""
        self.requires: List[str] = list(members["requires"])
        """tasks we consider when determining a changeset; also used to wait for completion in circleci workflow jobs"""
        self.service: NWService = service
        """parent cicd.yml/nwservice that generated this task"""
        self.id: str = name
        """the unprocessed task name as ID"""
        self.not_changed_command: Optional[Dict[str,
                                                Any]] = members["not_changed_command"]

        if isinstance(self.commands[0], str):
            raise Exception(
                f"Found a string only command named '{self.commands[0]}'! This should have been converted in the schema validation!!!")

        first_command_name = next(iter(self.commands[0]))

        self.name = f"{self.service.name}-{name}-{first_command_name}-job"
        """name of the task including the service name"""

        config_commands = self.service.context.general_config['commands']
        # set working dir default values
        for command in self.commands:
            for command_name, parameters in command.items():
                if "working_dir" not in parameters:
                    parameters["working_dir"] = self.path
                else:
                    # prepend service path
                    parameters["working_dir"] = os.path.normpath(os.path.join(self.service.path, str(parameters["working_dir"])
                                                                              )).replace("\\", "/").replace("//", "/")

                # set unittest-dir if existent in the command defined in 'general-config.yml'
                if "unittest_dir" in config_commands[command_name]['parameters']:
                    test_path = self.test_path
                    if "unittest_dir" not in parameters and len(test_path) > 0:  # prevent override
                        parameters["unittest_dir"] = test_path

        # always add the tasks directory as dependency
        self.dependencies.append(self.path + "/*")

    @ property
    def command_steps(self) -> List[Union[str, Dict[str, Any]]]:
        steps: List[Union[str, Dict[str, Any]]] = []

        # command dictionaries with parameters
        for command_entry in self.commands:
            for command, parameters in command_entry.items():
                step = {
                    command:
                    {
                        name: value for name, value in parameters.items()
                    }
                }
                steps.append(step)

        return steps

    @ property
    def is_feature_branch(self) -> bool:
        return self.service.context.job_context == Context.FEATURE

    @property
    def is_deployment(self) -> bool:
        return "deploy" in [name.lower() for command in self.commands for name in command.keys()]

    @ property
    async def should_execute_async(self) -> bool:
        """Returns true if dependencies changed"""
        return not(self.is_deployment and (self.is_feature_branch or self.service.context.fake_deploy)
                   ) and await self.is_changed_async

    async def check_task_changed_async(self, tasks: List["NWTask"]) -> Tuple[bool, Dict[str, Any]]:
        """get information about task change; returns a Tuple(True, reasons of change)"""

        if self.service.context.force:
            return (True, {"Forced":  "All apps changed"})

        async def to_result(routine: Coroutine[Any, Any, bool], name: str) -> Tuple[bool, str]:
            return (await routine, name)

        app_changed_info: Dict[str, Any] = {}
        result = await asyncio.gather(*[to_result(t.is_changed_async, t.name) for t in tasks])
        # filter results indicating a change only
        changed_result = list(filter(lambda x: x[0], result))

        is_changed = any(changed_result)
        if(is_changed):
            app_changed_info |= {
                "Tasks changed": list(map(lambda x: x[1], changed_result))
            }

        return (is_changed, app_changed_info)

    @ property
    async def is_changed_async(self) -> bool:
        if self.service.context.force:
            self.change_info = {"Forced": ""}
            return True

        # we need this critical section to wait for complete resolution of this if block
        # otherwise the first dependency check could set self._is_changed to a result,
        # which is not the final end result...
        async with self._lock:
            if self._is_changed is None:
                # handle dotnet related tasks:
                dotnet_result = await check_dotnet_change_async(
                    self.service.context.circleci_context,
                    self.path)
                self.change_info |= dotnet_result[1]
                self._is_changed = self._is_changed or dotnet_result[0]

                # handle dependencies given via configuration:
                dependency_result = await check_change_async(
                    self.service.context.circleci_context,
                    self.name, self.dependencies, name="dependencies")
                self.change_info |= dependency_result[1]
                self._is_changed = self._is_changed or dependency_result[0]

                # only check global dependencies if in layer 0
                if len(self.service.get_preceding_layers_references_for(self.id)) == 0:
                    global_result = await check_change_async(
                        self.service.context.circleci_context,
                        self.name, self.service.context.global_dependencies, name="global")
                    self._is_changed = self._is_changed or global_result[0]
                    self.change_info |= global_result[1]

                # check depending internal and external tasks by the requires attribute:
                required_dependencies_result = await self.service.check_changes_for_required(self.requires)
                self.change_info |= required_dependencies_result[1]
                self._is_changed = self._is_changed or required_dependencies_result[0]

                if self._is_changed:
                    print(
                        f'Detected relevant changes for {self.name}:\n{json.dumps(self.change_info, indent=2)}')
                else:
                    print(f"Detected no relevant changes for {self.name}")

        return self._is_changed

    @ property
    def test_path(self) -> str:
        """Returns the path to a test project from self.path or self.service.path else '' """
        def find_with_name_on_path(name: str, path: Path) -> str:
            name = re.sub("[\\.\\-_]", "", name)
            test_projects = list(map(lambda x: str(x), path.rglob(
                f"*.Test.csproj")))  # case sensitive names
            service_result = list(filter(lambda a_path: re.match(
                f".*{name}\\.test.*", str(a_path), flags=re.IGNORECASE), test_projects))
            return str(service_result.pop()).replace("\\", "/") if len(service_result) else ""

        result = find_with_name_on_path(self.id, Path(self.path))
        if not len(result):
            result = find_with_name_on_path(
                self.id, Path(self.service.path))
        # result = result if len(result) else self.path
        print(
            f'Test project for {self.name}: {result if len(result) else "None"}')
        return result

    async def task_to_yaml_async(self) -> Dict[str, Any]:
        def to_yaml(commands: List[Union[str, Dict[str, Any]]]) -> Dict[str, Any]:
            steps: List[Union[str, Dict[str, Any]]] = ["checkout"]
            steps += commands
            steps.insert(1, {
                "changeset_info": {
                    "file_name": "change-set.json",
                    "data": json.dumps(self.change_info)
                }})
            yml_obj = {
                "executor": self.executor,
                "resource_class": self.resource_class,
                "steps": steps
            }

            # self.add_docker_push(task, steps)
            return {self.name: yml_obj}

        if await self.should_execute_async:
            return to_yaml(self.command_steps)

        # empty job
        if self.not_changed_command:
            return to_yaml([self.not_changed_command])

        reason = "# No changes to code, infrastructure or dependencies detected"
        if self.is_feature_branch:
            reason = "# you are working on a feature branch"
        elif self.is_deployment and self.service.context.fake_deploy:
            reason = f"\necho -e '{FAKE_DEPLOY_MSG}'"

        return {
            self.name:
            {
                "docker": [{"image": "cimg/base:stable"}],
                "resource_class": "small",
                "steps": [
                    {
                        "empty_job":
                        {
                            "job_name": self.name,
                            "reason": reason
                        }
                    }
                ]
            }
        }


FAKE_DEPLOY_MSG: str = '''
~~~~           FAKE DEPLOY          ~~~~


░░░░░░░░░░░░░░▄▄▄▄▄▄▄▄▄▄▄▄░░░░░░░░░░░░░░
░░░░░░░░░░░░▄████████████████▄░░░░░░░░░░
░░░░░░░░░░▄██▀░░░░░░░▀▀████████▄░░░░░░░░
░░░░░░░░░▄█▀░░░░░░░░░░░░░▀▀██████▄░░░░░░
░░░░░░░░░███▄░░░░░░░░░░░░░░░▀██████░░░░░
░░░░░░░░▄░░▀▀█░░░░░░░░░░░░░░░░██████░░░░
░░░░░░░█▄██▀▄░░░░░▄███▄▄░░░░░░███████░░░
░░░░░░▄▀▀▀██▀░░░░░▄▄▄░░▀█░░░░█████████░░
░░░░░▄▀░░░░▄▀░▄░░█▄██▀▄░░░░░██████████░░
░░░░░█░░░░▀░░░█░░░▀▀▀▀▀░░░░░██████████▄░
░░░░░░░▄█▄░░░░░▄░░░░░░░░░░░░██████████▀░
░░░░░░█▀░░░░▀▀░░░░░░░░░░░░░███▀███████░░
░░░▄▄░▀░▄░░░░░░░░░░░░░░░░░░▀░░░██████░░░
██████░░█▄█▀░▄░░██░░░░░░░░░░░█▄█████▀░░░
██████░░░▀████▀░▀░░░░░░░░░░░▄▀█████████▄
██████░░░░░░░░░░░░░░░░░░░░▀▄████████████
██████░░▄░░░░░░░░░░░░░▄░░░██████████████
██████░░░░░░░░░░░░░▄█▀░░▄███████████████
███████▄▄░░░░░░░░░▀░░░▄▀▄███████████████

~~~~           FAKE DEPLOY          ~~~~
'''
