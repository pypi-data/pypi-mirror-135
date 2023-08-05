import os
from dataclasses import dataclass, field


@dataclass
class CircleCIContext:
    branch: str
    build_num: int
    project_reponame: str
    project_username: str
    workflow_id: str
    working_directory: str
    circle_token: str
    github_token: str
    vcs_type: str = "gh"
    current_vcs_revision: str = field(default="", init=False)
    last_successful_vcs_revision: str = field(default="", init=False)

    @staticmethod
    def create_from_environ() -> "CircleCIContext":
        return CircleCIContext(
            branch=os.environ["CIRCLE_BRANCH"],
            build_num=int(os.environ["CIRCLE_BUILD_NUM"]),
            project_reponame=os.environ["CIRCLE_PROJECT_REPONAME"],
            project_username=os.environ["CIRCLE_PROJECT_USERNAME"],
            workflow_id=os.environ["CIRCLE_WORKFLOW_ID"],
            working_directory=os.environ["CIRCLE_WORKING_DIRECTORY"],
            circle_token=os.environ["CIRCLE_TOKEN"],
            github_token=os.environ["GITHUB_TOKEN"])

    @staticmethod
    def create_dummy_env() -> "CircleCIContext":
        circle_token = os.environ.get("CIRCLE_TOKEN", "")
        github_token = os.environ.get("GITHUB_TOKEN", "")
        return CircleCIContext(
            branch="develop",
            build_num=1,
            project_reponame="nw-platform",
            project_username="nativewaves",
            workflow_id="2239e3f4-dbd4-4879-b614-298584b884c2",
            working_directory=".",
            circle_token=circle_token,
            github_token=github_token)
