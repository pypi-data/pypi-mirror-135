from typing import Any, Dict, List, Tuple

import aiohttp

from nwcicdsetup.circleciapiclient import CircleCIAPIClient
from nwcicdsetup.circlecicontext import CircleCIContext
from nwcicdsetup.dotnetdependencyresolver import fetch_dependencies
from nwcicdsetup.githubapiclient import GitHubAPIClient


async def init_async(dummy_env: bool, forced : bool) -> CircleCIContext:
    if dummy_env:
        context = CircleCIContext.create_dummy_env()
        print("Created dummy circleci context")
    else:
        context = CircleCIContext.create_from_environ()

    if forced:
        return context

    async with aiohttp.ClientSession() as session:
        circleci_client = CircleCIAPIClient(session, context)
        current_job = await circleci_client.load_job_async(context.build_num)
        last_successful_vcs = await circleci_client.load_previous_successful_vcs(current_job)
        context.current_vcs_revision = current_job.vcs_revision
        context.last_successful_vcs_revision = last_successful_vcs

        print(
            f"Current build url '{current_job.web_url}' for job '{current_job.name}'")
        if last_successful_vcs:
            print(
                f"Last successful vcs '{last_successful_vcs}'")

        await session.close()

    return context


async def check_dotnet_change_async(circleci_context: CircleCIContext, project_dir: str) -> Tuple[bool, Dict[str, Any]]:
    if not circleci_context.last_successful_vcs_revision:
        print(
            f"No previous successful build found - Assume {project_dir} changed!!!")
        return (True, {"Check change": "No previous successful build found"})

    try:
        dotnet_dependencies = fetch_dependencies(
            root_dir=circleci_context.working_directory,
            project_dir=project_dir)
    except Exception as e:
        print(f"{e.args}")
        return (False, {})

    dotnet_dependencies = list(set(dotnet_dependencies))  # cut duplicates
    if len(dotnet_dependencies) <= 0:
        return (False, {})

    dotnet_dependencies.sort()

    async with aiohttp.ClientSession() as session:

        github_client = GitHubAPIClient(session, circleci_context.github_token)

        # don't... just don't: https://youtu.be/KD_1Z8iUDho?t=216
        # if not await github_client.check_dependencies_async(context.project_username, context.project_reponame, context.branch, custom_dependencies):
        #     print("Invalid given custom dependencies - Interrupting")
        #     raise Exception(
        #         f"Invalid given dependencies {json.dumps(custom_dependencies, indent=4)}")

        changeset = await github_client.get_changeset(
            circleci_context.current_vcs_revision,
            circleci_context.last_successful_vcs_revision,
            circleci_context.project_reponame,
            circleci_context.project_username)

        # print(
        # f"Check-changes on branch '{circleci_context.branch}' on '{project_dir}' with dotnet dependencies:\n{json.dumps(dotnet_dependencies, indent=4)} custom dependencies:\n{json.dumps(custom_dependencies, indent=4)}")

        relevant_changes: List[str] = changeset.find_relevant_changes(
            dotnet_dependencies)
        # if len(relevant_dotnet + relevant_custom):
        #     print(
        #         f"Detected relevant changes for {project_dir}: {json.dumps(relevant_dotnet + relevant_custom, indent=4)}")
        # else:
        #     print(f"No relevant changes for {project_dir}")
        await session.close()
        if len(relevant_changes):
            return (True, {"dotnet dependencies": relevant_changes})
        return (False, {})


async def check_change_async(circleci_context: CircleCIContext, project_name: str, dependencies: List[str], name: str) -> Tuple[bool, Dict[str, Any]]:
    if not circleci_context.last_successful_vcs_revision:
        print(
            f"No previous successful build found - Assume {project_name} changed!!!")
        return (True, {"Check change": "No previous successful build found"})

    if len(dependencies) <= 0:
        return (False, {})

    dependencies.sort()

    async with aiohttp.ClientSession() as session:
        github_client = GitHubAPIClient(session, circleci_context.github_token)

        changeset = await github_client.get_changeset(
            circleci_context.current_vcs_revision,
            circleci_context.last_successful_vcs_revision,
            circleci_context.project_reponame,
            circleci_context.project_username)

        await session.close()
        # print(
        #     f"Dependencies for {project_name}: {json.dumps(dependencies, indent=4)}")

        relevant_changes: List[str] = changeset.find_relevant_changes(
            dependencies)
        if len(relevant_changes):
            return (True, {name: relevant_changes})

        return (False, {})
