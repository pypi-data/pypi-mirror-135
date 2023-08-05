import asyncio
import fnmatch
from typing import Any, Dict, List, Optional

import aiohttp


class GitHubChangeset:

    def __init__(self, url: str, headers: Dict[str, Any], session: Optional[aiohttp.ClientSession] = None) -> None:
        self.url = url
        self.headers = headers
        self.session = session if session is not None else aiohttp.ClientSession()
        self.filenames : List[str] = []

    async def fetch_async(self) -> None:
        """Queries the changeset and returns the a list of changed files"""
        print(f"Checking change-set for: '{self.url}'")
        for _ in range(3):
            async with self.session.get(self.url, headers=self.headers) as response:
                try:
                    data = await response.json()
                    response.raise_for_status()
                    
                    for item in data.get("files", []):
                        self.filenames.append(item["filename"])
                    return
                except aiohttp.ServerConnectionError as e:
                    print(e)
                    await asyncio.sleep(5)
                except aiohttp.ClientConnectionError as e:
                    print(e)
                    await asyncio.sleep(5)
                except Exception as e:
                    print(e)
                    await asyncio.sleep(5)
        raise Exception(f"Could not load changeset for '{self.url}'")

    def join(self, other : "GitHubChangeset") -> "GitHubChangeset":
        self.filenames += other.filenames
        return self

    def find_relevant_changes(self, dependencies: List[str]) -> List[str]:
        relevant_changes: List[str] = []

        dependencies = list(filter(None, dependencies))
        matches: List[str] = []
        for pattern in [x for x in dependencies if x[0] != "!"]:
            for match in fnmatch.filter(self.filenames, pattern):
                matches.append(match)

        unmatch: List[str] = []
        for pattern in [x[1:] for x in dependencies if x[0] == "!"]:
            for match in fnmatch.filter(matches, pattern):
                unmatch.append(match)

        relevant_changes = list(set(matches).difference(set(unmatch)))
        relevant_changes.sort()
        return relevant_changes
