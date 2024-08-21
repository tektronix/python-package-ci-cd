"""Update the development dependencies.

This script will update the development dependencies that are pinned in the pyproject.toml and .pre-
commit-config.yaml files.

In order to use this script, you must be using the poetry package manager and `poetry` must be
accessible on the commandline. If you want to use this script to update pre-commit dependencies,
`pre-commit` must be installed in the current Python environment.
"""

from __future__ import annotations

import contextlib
import json
import os
import shlex
import subprocess
import sys
import warnings

from pathlib import Path

from pypi_simple import PyPISimple
from yamlfix import fix_files  # pyright: ignore[reportUnknownVariableType]

_ENV_VAR_TRUE_VALUES = {"1", "true", "yes"}


def _convert_dict_input(input_str: str) -> dict[str, list[str]]:
    """Parse the input string into a dictionary of the required type.

    Args:
        input_str: The input string to parse.

    Returns:
        The parsed dictionary.

    Raises:
        ValueError: If the input string does not match the required format.
    """
    try:
        # Convert the string to a dictionary using ast.literal_eval for safety
        result_dict = json.loads(input_str)

        # Check if the result is a dictionary with the correct type
        if isinstance(result_dict, dict) and all(
            isinstance(k, str) and isinstance(v, list) and all(isinstance(i, str) for i in v)  # pyright: ignore[reportUnknownVariableType]
            for k, v in result_dict.items()  # pyright: ignore[reportUnknownVariableType]
        ):
            return result_dict  # pyright: ignore[reportUnknownVariableType]
        raise ValueError  # noqa: TRY301
    except (SyntaxError, ValueError) as e:
        msg = f'Input "{input_str}" does not match the required ' f"type of `dict[str, list[str]]`."
        raise ValueError(msg) from e


def _run_cmd_in_subprocess(command: str) -> None:
    """Run the given command in a subprocess.

    Args:
        command: The command string to send.
    """
    command = command.replace("\\", "/")
    print(f"\nExecuting command: {command}")
    subprocess.check_call(shlex.split(command))  # noqa: S603


def _update_poetry_dependencies(
    python_executable: str,
    repository_root_directory: Path,
    dependencies_to_update: dict[str, list[str]],
    *,
    lock_only: bool,
) -> None:
    """Update the specified dependencies via poetry in the pyproject.toml file.

    This will also fix the formatting of the pyproject.toml file using the `toml-sort` package.

    Args:
        python_executable: The path to the python executable to use.
        repository_root_directory: The root directory of the repository.
        dependencies_to_update: A dictionary of dependency groups to update, where each key is a
            group and each value is a tuple of dependencies to update within that group.
        lock_only: A boolean indicating if only the lock file should be updated.
    """
    pypi_server = PyPISimple()

    # Remove the dependencies from poetry to avoid issues if they are in multiple groups
    for group, dependencies_list in dependencies_to_update.items():
        dependencies = " ".join(f'"{x.split("[", maxsplit=1)[0]}"' for x in dependencies_list)
        group_arg = f" --group={group}" if group else ""
        _run_cmd_in_subprocess(
            f'"{python_executable}" -m poetry remove --lock{group_arg} {dependencies}',
        )

    # Get the latest versions for each of the dependencies to update
    for group, dependencies_list in dependencies_to_update.items():
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
        group_arg = f" --group={group}" if group else ""
        poetry_add_cmd = f'"{python_executable}" -m poetry add{group_arg} {dependencies}'
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
    _run_cmd_in_subprocess(
        f"git config --global --add safe.directory "
        f'"{repository_root_directory.resolve().as_posix()}"'
    )
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
            lines = sorted(file.readlines(), key=lambda x: x.lower().split("==")[0])
        with file_path.open("w") as file:
            file.writelines(lines)

    _run_cmd_in_subprocess(f'"{python_executable}" -m poetry config warnings.export false')

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


def main(
    repo_root: str,
    dependency_dict: dict[str, list[str]],
    export_dependency_groups: list[str],
    pre_commit_hook_skip_list: str,
    *,
    install_dependencies: bool,
    run_pre_commit: bool,
    update_pre_commit: bool,
) -> None:
    """Run the script to update the development dependencies."""
    python_executable = sys.executable

    repo_root_path = Path(repo_root).resolve()
    os.chdir(repo_root_path)
    print(f"\nUpdating development dependencies in {Path.cwd()}")

    _update_poetry_dependencies(
        python_executable,
        repo_root_path,
        dependency_dict,
        lock_only=not install_dependencies,
    )
    if update_pre_commit or run_pre_commit:
        _update_pre_commit_dependencies(python_executable, repo_root_path)
    if export_dependency_groups:
        _export_requirements_files(python_executable, export_dependency_groups)
    if run_pre_commit:
        # Run the pre-commit hooks, ignore any errors since they are
        # just being run to auto-fix files.
        with contextlib.suppress(subprocess.CalledProcessError):
            os.environ["SKIP"] = pre_commit_hook_skip_list
            _run_cmd_in_subprocess(f'"{python_executable}" -m pre_commit run --all-files')


if __name__ == "__main__":
    # Run the main function
    # See https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables
    main(
        repo_root=os.environ["INPUT_REPO-ROOT"],
        dependency_dict=_convert_dict_input(os.environ["INPUT_DEPENDENCY-DICT"]),
        export_dependency_groups=[
            x for x in os.environ["INPUT_EXPORT-DEPENDENCY-GROUPS"].split(",") if x
        ],
        pre_commit_hook_skip_list=os.environ["INPUT_PRE-COMMIT-HOOK-SKIP-LIST"],
        install_dependencies=os.environ["INPUT_INSTALL-DEPENDENCIES"].lower()
        in _ENV_VAR_TRUE_VALUES,
        run_pre_commit=os.environ["INPUT_RUN-PRE-COMMIT"].lower() in _ENV_VAR_TRUE_VALUES,
        update_pre_commit=os.environ["INPUT_UPDATE-PRE-COMMIT"].lower() in _ENV_VAR_TRUE_VALUES,
    )
