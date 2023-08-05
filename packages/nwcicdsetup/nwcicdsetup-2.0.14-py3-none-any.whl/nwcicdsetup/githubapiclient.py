import asyncio
import json
from typing import Any, Dict, List
from urllib.parse import quote

import aiohttp

from nwcicdsetup.githubchangeset import GitHubChangeset


class GitHubAPIClient:

    def __init__(self, session: aiohttp.ClientSession, auth_token: str) -> None:
        self._base_url = "https://api.github.com"
        self._auth_token = auth_token
        self._session = session

    @property
    def headers(self) -> Dict[str, Any]:
        return {
            "Authorization": "token {}".format(self._auth_token)
        }

    async def check_dependencies_async(self, username: str, repository: str, branch: str, dependencies: List[str]) -> bool:
        tasks = [self.check_dependency_async(username, repository, branch, d)
                 for d in dependencies]
        print("check dependencies for branch {}".format(quote(branch)))
        return all(await asyncio.gather(*tasks))

    async def check_dependency_async(self, username: str, repository: str, branch: str, dependency: str) -> bool:
        """Use GitHub to verify that a dependency is valid"""
        if dependency.endswith("/*"):
            dependency = dependency[:-2]

        url: str = "{}/repos/{}/{}/contents/{}?ref={}".format(
            self._base_url,
            quote(username),
            quote(repository),
            quote(dependency),
            quote(branch))

        for _ in range(5):
            async with self._session.get(url, headers=self.headers) as response:
                try:
                    response.raise_for_status()
                    return True
                except aiohttp.ClientResponseError as e:
                    print("Status {}: Reattempt resource '{}':\n{}".format(
                        e.status, quote(dependency), e.message))  # type: ignore
                    await asyncio.sleep(5)
                except aiohttp.ServerConnectionError:
                    await asyncio.sleep(5)
                except aiohttp.ClientConnectionError:
                    await asyncio.sleep(5)

        print("~~~ Invalid resource '{}' ~~~".format(quote(dependency)))
        return False

    async def get_changeset(
            self,
            commit_id: str,
            previous_commit_id: str,
            repository: str,
            username: str) -> GitHubChangeset:
        """Use GitHub to get all changes between two commit ids"""
        cache: Dict[Any, Any]
        lock: asyncio.Lock

        _globals = globals()
        if not "__changeset_cache" in _globals:
            _globals["__changeset_cache"] = cache = {}
        else:
            cache = _globals["__changeset_cache"]

        if not "__changeset_lock" in cache:
            cache["__changeset_lock"] = lock = asyncio.Lock()
        else:
            lock = cache["__changeset_lock"]

        async with lock:
            cache_key = (commit_id, previous_commit_id, repository, username)
            if cache_key in cache:
                return cache[cache_key]

            # the reason to flip the commit ids are merge requests. The api expects us to use a commit id that timely
            # happened before the second. To prevent additional checks, we just check both possibilities
            changeset1 = GitHubChangeset(
                f"{self._base_url}/repos/{quote(username)}/{quote(repository)}/compare/{quote(previous_commit_id)}...{quote(commit_id)}", self.headers, self._session)
            changeset2 = GitHubChangeset(
                f"{self._base_url}/repos/{quote(username)}/{quote(repository)}/compare/{quote(commit_id)}...{quote(previous_commit_id)}", self.headers, self._session)

            await asyncio.gather(*[changeset1.fetch_async(), changeset2.fetch_async()])
            result = changeset1.join(changeset2)
            cache[cache_key] = result
            print(
                f"Found new changeset for commits between '{previous_commit_id}' and '{commit_id}': {json.dumps(result.filenames, indent=4)}")
            return result
