import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

from nwcicdsetup import circleci
from nwcicdsetup.nwservice import NWService, NWServiceContext
from nwcicdsetup.validationschema import general_config_validate


def errprint(*args: Any, **kwargs: Any):
    print(*args, file=sys.stderr, **kwargs)


def str_presenter(dumper: Any, data: Any):
    if '\n' in data:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


async def generate(outfile: str, general_config_path: str, global_dependencies: List[str], fake_deploy: bool, force: bool, dummy_env: bool) -> None:
    print(
        f"Global dependencies: {json.dumps(global_dependencies, indent=4)}")
    if force:
        print("<<< Forcing job execution >>>")
    if fake_deploy:
        print("<<< Using fake deploy >>>")
    if dummy_env:
        print("<<< Using dummy environment >>>")

    print(f"writing config to '{outfile}'")
    print(f"Load general config from '{general_config_path}'")

    try:
        yaml.add_representer(str, str_presenter)
        yaml.representer.SafeRepresenter.add_representer(  # type: ignore
            str, str_presenter)

        circleci_context = await circleci.init_async(dummy_env, force)
        cwd = Path(".")
        configs = list(cwd.rglob("cicd.yml")) + \
            list(cwd.rglob("cicd.yaml")) + list(cwd.rglob("cicd.json"))
        print(f"found {len(configs)} 'cicd' configs in {cwd.resolve()}")

        if not os.path.exists(general_config_path):
            raise Exception(
                f"No file found for general config at '{general_config_path}'")

        with open(general_config_path, mode="rb") as general_config_stream:
            print(f"process general config '{general_config_path}'")
            general_config = general_config_validate(
                yaml.safe_load(general_config_stream))

        services: Dict[str, NWService] = {}
        context = NWServiceContext(circleci_context, services, general_config, str(
            cwd.resolve()), global_dependencies, fake_deploy, force)
        services |= {s.name: s for s in [NWService(context, str(
            configPath.relative_to(cwd))) for configPath in configs]}

        # preserve entries from loaded base config
        workflow_name = "{}-build-deploy".format(
            NWServiceContext.branch_to_context(circleci_context.branch).name.lower())
        workflow_jobs: List[Dict[str, Any]] = []
        jobs: Dict[str, Any] = {}

        if "workflows" not in general_config:
            general_config["workflows"] = {
                workflow_name: {"jobs": workflow_jobs}}
        if workflow_name not in general_config["workflows"]:
            general_config["workflows"][workflow_name] = {
                "jobs": workflow_jobs}

        general_config["workflows"]["version"] = 2.1  # type: ignore

        if "jobs" not in general_config:
            general_config["jobs"] = jobs

        # generate jobs section
        yml_tasks = [asyncio.create_task(s.job_yaml_async())
                     for s in services.values()]
        for t_jobs in await asyncio.gather(*yml_tasks):
            jobs |= t_jobs

        # generate workflows section
        yml_tasks = [s.workflow_jobs_async() for s in services.values()]
        for w_jobs in await asyncio.gather(*yml_tasks):
            workflow_jobs += w_jobs

        # output
        yaml_str: str = yaml.safe_dump(general_config, width=1000  # type: ignore
                                       )
        with open(os.path.join(cwd.resolve(), f"{outfile}"), mode="w") as config_file:
            config_file.write(yaml_str)
            print(f"Wrote configuration to {outfile}")
    except Exception as e:
        errprint(str(e))
        exit(1)
