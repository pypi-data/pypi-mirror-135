import asyncio
import json
from typing import Any, Dict, List, Optional, Set
from urllib.parse import quote

import aiohttp

from nwcicdsetup.circlecicontext import CircleCIContext
from nwcicdsetup.circlecijob import CircleCIJob


class CircleCIAPIClient:

    def __init__(self, session: aiohttp.ClientSession, context: CircleCIContext) -> None:
        self._base_url_v2 = "https://circleci.com/api/v2"
        self._base_url_v1_1 = "https://circleci.com/api/v1.1"
        self._session = session
        self._context = context

    @ property
    def headers(self) -> Dict[str, Any]:
        return {"Circle-Token": self._context.circle_token}

    @ property
    def project_slug(self) -> str:
        return "{}/{}/{}".format(
            quote(self._context.vcs_type),
            quote(self._context.project_username),
            quote(self._context.project_reponame))

    async def load_workflow_name_async(self) -> str:
        url = f"{self._base_url_v2}/workflow/{quote(self._context.workflow_id)}"
        async with self._session.get(url, headers=self.headers) as response:
            response.raise_for_status()
            response_data = await response.text()
            data = json.loads(response_data)
            return data["name"]

    async def load_job_async(self, job_number: int) -> CircleCIJob:
        job_url = f"{self._base_url_v2}/project/{self.project_slug}/job/{job_number}"
        job: Optional[CircleCIJob] = None

        for _ in range(5):
            async with self._session.get(job_url, headers=self.headers) as response:
                try:
                    response_data = await response.text()
                    response.raise_for_status()
                    data = json.loads(response_data)
                    job = CircleCIJob.from_data(data)
                except aiohttp.ClientResponseError as e:
                    print("Maybe the circleci-token is wrong?!")
                    print(
                        f"Status {e.status}: Reattempt resource '{job_url}': {e.message}")  # type: ignore
                    await asyncio.sleep(5)

        if not job:
            raise Exception(f"Could not query job for {job_url}")

        pipeline_url: str = f"{self._base_url_v2}/pipeline/{job.pipeline_id}"
        for _ in range(5):
            async with self._session.get(pipeline_url, headers=self.headers) as response:
                try:
                    response_data = await response.text()
                    response.raise_for_status()
                    data = json.loads(response_data)
                    job.vcs_revision = data["vcs"]["revision"]
                    job.trigger_type = data["trigger"]["type"]
                except aiohttp.ClientResponseError as e:
                    print("Maybe the circleci-token is wrong?!")
                    print(
                        f"Status {e.status}: Reattempt resource '{pipeline_url}': {e.message}")  # type: ignore
                    await asyncio.sleep(5)

        return job

    async def load_previous_successful_vcs(self, job: CircleCIJob) -> str:
        # conn.request("GET", "/api/v2/pipeline/%7Bpipeline-id%7D/workflow?page-token=SOME_STRING_VALUE", headers=headers)
        header = {
            "Circle-Token": f"{self._context.circle_token}"
        }
        print("try to find previous successful build...")

        async def search() -> Optional[Dict[str, Any]]:
            page_token: str = ""
            print("search")
            wait_count = 0

            while page_token != None:
                page_token = f"?page-token={page_token}&" if len(
                    page_token) else "?"
                get_all_pipelines_url = f"{self._base_url_v2}/project/{self.project_slug}/pipeline{page_token}branch={quote(self._context.branch)}"
                print(f"request: '{get_all_pipelines_url}'")
                async with self._session.get(get_all_pipelines_url, headers=header) as response:
                    response.raise_for_status()
                    response_data = json.loads(await response.text())
                    if not len(response_data) or not len(response_data["items"]):
                        if wait_count >= 3:
                            print(
                                f"Could not fetch results for '{get_all_pipelines_url}'")
                            break
                        else:
                            wait_count = wait_count + 1
                            print(
                                f"Empty response... retry attempt {wait_count}/3")
                            await asyncio.sleep(0.5)
                            continue

                    page_token = response_data["next_page_token"]

                    def filter_func(pipeline: Dict[str, Any]) -> bool:
                        return len(pipeline["errors"]) == 0 and pipeline["state"] == "created" and pipeline["vcs"]["branch"] == self._context.branch

                    result: List[Dict[str, Any]] = list(
                        filter(filter_func, response_data["items"]))
                    print(
                        f"Considering {len(result)} pipelines for processing")

                    for r in result:
                        get_workflows_url = f"{self._base_url_v2}/pipeline/{r['id']}/workflow"
                        async with self._session.get(get_workflows_url, headers=header) as response:
                            info = {
                                "pipeline-id": r['id'],
                                "revision": r['vcs']['revision'],
                                "commit": r['vcs']['commit'] if "commit" in r['vcs'] else "<Branch creation>"
                            }
                            print(
                                f"Check pipeline {json.dumps(info, indent=3)}")
                            print(
                                f"Request workflow status for '{get_workflows_url}'")

                            response.raise_for_status()
                            response_data = json.loads(await response.text())

                            unique_names: Set[str] = set([i["name"]
                                                          for i in response_data["items"]])
                            status = [(i["name"], i["status"])
                                      for i in response_data["items"]]
                            print(
                                f"Considering workflows: {json.dumps(status)}")

                            success_pipelines = [any([n == xi["name"] and xi["status"] == "success"
                                                      for xi in response_data["items"]]) for n in unique_names]

                            if all(success_pipelines):
                                print(
                                    f"Found a successful pipeline {json.dumps(info, indent=3)}")
                                return r

        success = await search()
        return success["vcs"]["revision"] if success != None else ""
