"""Update the development dependencies.

This script will update the development dependencies that are pinned in the pyproject.toml and .pre-
commit-config.yaml files.
"""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
import warnings

from pathlib import Path

from pypi_simple import PyPISimple
from yamlfix import fix_files  # pyright: ignore[reportUnknownVariableType]

DEPENDENCIES_TO_UPDATE: dict[str, tuple[str, ...]] = {  # TODO: convert to inputs
}


def _parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments.

    Returns:
        The parsed Namespace.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        action="store",
        dest="repo_root",
        type=Path,
        required=True,
        help="The root directory of the repository.",
    )
    parser.add_argument(
        "--no-install",
        action="store_true",
        dest="no_install",
        help="Indicate if packages should not be installed via poetry (Primarily used in CI).",
    )
    parser.add_argument(
        "--export-dependency-group",
        dest="dependency_groups",
        action="append",
        help=(
            "Specify a poetry dependency group to export the requirements for. An output "
            "folder can be specified by adding a ':' and the custom output folder path to "
            'the provided group name, e.g. "tests:custom/folder/path". The created file will '
            'always be named "requirements.txt", and the folder will default to matching the '
            "group name if no custom folder path is given. "
            "Use the flag multiple times for multiple groups."
        ),
    )

    return parser.parse_args()


def _run_cmd_in_subprocess(command: str) -> None:
    """Run the given command in a subprocess.

    Args:
        command: The command string to send.
    """
    command = command.replace("\\", "/")
    print(f"\nExecuting command: {command}")
    subprocess.check_call(shlex.split(command))  # noqa: S603


def _update_poetry_dependencies(
    python_executable: str, repository_root_directory: Path, *, lock_only: bool
) -> None:
    """Update the specified dependencies via poetry in the pyproject.toml file.

    This will also fix the formatting of the pyproject.toml file using the `toml-sort` package.

    Args:
        python_executable: The path to the python executable to use.
        repository_root_directory: The root directory of the repository.
        lock_only: A boolean indicating if only the lock file should be updated.
    """
    pypi_server = PyPISimple()

    # Remove the dependencies from poetry to avoid issues if they are in multiple groups
    for group, dependencies_list in DEPENDENCIES_TO_UPDATE.items():
        dependencies = " ".join(f'"{x.split("[", maxsplit=1)[0]}"' for x in dependencies_list)
        _run_cmd_in_subprocess(
            f'"{python_executable}" -m poetry remove --lock --group={group} {dependencies}',
        )

    # Get the latest versions for each of the dependencies to update
    for group, dependencies_list in DEPENDENCIES_TO_UPDATE.items():
        latest_dependency_versions: list[str] = []
        for dependency in dependencies_list:
            latest_dep_version = (
                pypi_server.get_project_page(dependency.split("[", maxsplit=1)[0])
                .packages[-1]
                .version
            )
            latest_dependency_versions.append(dependency + f"=={latest_dep_version}")

        # Update dependencies in pyproject.toml using poetry
        dependencies = " ".join(f'"{x}"' for x in latest_dependency_versions)
        poetry_add_cmd = f'"{python_executable}" -m poetry add --group={group} {dependencies}'
        if lock_only:
            poetry_add_cmd += " --lock"
        _run_cmd_in_subprocess(poetry_add_cmd)

    # Run poetry update
    poetry_update_cmd = f'"{python_executable}" -m poetry update'
    if lock_only:
        poetry_update_cmd += " --lock"
    _run_cmd_in_subprocess(poetry_update_cmd)

    # Fix the formatting of the pyproject.toml file
    python_script_location = Path(python_executable).parent
    _run_cmd_in_subprocess(
        f'"{python_script_location}/toml-sort" '
        f'"{repository_root_directory}/pyproject.toml" --in-place --sort-table-keys',
    )


def _update_pre_commit_dependencies(
    python_executable: str, repository_root_directory: Path
) -> None:
    """Update the pre-commit dependencies in the .pre-commit-config.yaml file.

    This function will also fix the formatting of the yaml file using the `yamlfix` package.

    Args:
        python_executable: The path to the python executable to use.
        repository_root_directory: The root directory of the repository.
    """
    # Update pre-commit config file
    _run_cmd_in_subprocess(f'"{python_executable}" -m pre_commit autoupdate --freeze')

    # Fix the formatting of the pre-commit config file
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        fix_files([f"{repository_root_directory}/.pre-commit-config.yaml"])


def _export_requirements_files(python_executable: str, dependency_groups: list[str]) -> None:
    """Export the requirements files for the specified dependency groups.

    This function uses the `poetry export` command to generate the requirements files for the
    specified dependency groups.

    Args:
        python_executable: The path to the python executable to use.
        dependency_groups: The list of dependency groups to export the requirements for.
    """

    def _sort_requirements_file(file_path: Path) -> None:
        """Sort the lines in the given requirements file.

        Args:
            file_path: The path to the requirements file to sort.
        """
        with file_path.open() as file:
            lines = sorted(file.readlines())
        with file_path.open("w") as file:
            file.writelines(lines)

    for group_output_pair in dependency_groups:
        if ":" in group_output_pair:
            group, output_folder = group_output_pair.split(":", maxsplit=1)
        else:
            group = group_output_pair
            output_folder = group
        _run_cmd_in_subprocess(
            f'"{python_executable}" -m poetry export --only {group} '
            f"--without-hashes --output {output_folder}/requirements.txt",
        )
        _sort_requirements_file(Path(f"{output_folder}/requirements.txt"))


def main() -> None:
    """Run the script to update the development dependencies."""
    python_executable = sys.executable

    args = _parse_arguments()

    _update_poetry_dependencies(python_executable, args.repo_root, lock_only=args.no_install)
    _update_pre_commit_dependencies(python_executable, args.repo_root)
    if args.dependency_groups:
        _export_requirements_files(python_executable, args.dependency_groups)


if __name__ == "__main__":
    main()
