import os
from pathlib import Path
from typing import List, Set, Union
from xml.etree import ElementTree


def fetch_dependencies(root_dir: str, project_dir: str) -> List[str]:
    proj_file_path = Implementation.find_proj_file_path(project_dir)
    paths = Implementation.load_references(proj_file_path)
    dependencies = Implementation.convert_references_to_dependencies(
        root_dir, paths)
    return dependencies


class Implementation:

    @staticmethod
    def normalize_path(path: Union[str, Path]) -> str:
        return str(path).replace("\\\\", "/").replace("\\", "/").replace(os.sep, "/")

    @staticmethod
    def resolve_path(path: str) -> str:
        return Implementation.normalize_path(Path(path).expanduser().resolve())

    @staticmethod
    def find_proj_file_path(project_dir: str) -> str:
        proj_file_name: str = ""

        results = list(Path(Implementation.normalize_path(project_dir))
                       .rglob("*.csproj"))

        if not len(results):
            raise Exception(
                f"Could not find *.csproj file in project directory '{project_dir}'")

        print(f"Resolve .net dependencies for: {results[0]}")
        proj_file_name = str(results[0])
        proj_file_path: str = Implementation.resolve_path(proj_file_name)

        if not os.path.exists(proj_file_path):
            raise Exception(f"{proj_file_path} does not exist!")
        return proj_file_path

    @staticmethod
    def load_references(proj_file_path: str, level: int = 0) -> List[str]:

        proj_file_path = Implementation.resolve_path(proj_file_path)
        project_dir = os.path.dirname(proj_file_path)

        tree = ElementTree.parse(proj_file_path)
        root = tree.getroot()

        paths: Set[str] = set()
        paths.add(proj_file_path)

        for project in root.iter('ProjectReference'):
            include_path = Implementation.normalize_path(
                project.attrib["Include"])
            ref_proj_file_path = Implementation.resolve_path(
                os.path.join(project_dir, include_path))
            paths.add(ref_proj_file_path)

            if level < 10:
                for path in Implementation.load_references(ref_proj_file_path, level + 1):
                    paths.add(path)

        return list(paths)

    @staticmethod
    def convert_references_to_dependencies(root_dir: str, paths: List[str]) -> List[str]:

        abs_root_dir = Implementation.resolve_path(root_dir)

        dependencies: Set[str] = set()
        for path in paths:
            abs_path = Implementation.resolve_path(path)
            project_dir = os.path.dirname(abs_path)
            dependency = project_dir
            if project_dir.startswith(abs_root_dir):
                dependency = dependency[len(abs_root_dir):]

            dependency = dependency.strip("/") + "/*"
            dependencies.add(dependency)

        return list(dependencies)
