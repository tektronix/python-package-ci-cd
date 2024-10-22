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

import yaml

from pypi_simple import PyPISimple
from yamlfix import fix_files  # pyright: ignore[reportUnknownVariableType]

_ENV_VAR_TRUE_VALUES = {"1", "true", "yes"}


def convert_dict_input(input_str: str) -> dict[str, list[str]]:
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


def run_cmd_in_subprocess(command: str) -> None:
    """Run the given command in a subprocess.

    Args:
        command: The command string to send.
    """
    command = command.replace("\\", "/")
    print(f"\nExecuting command: {command}")
    subprocess.check_call(shlex.split(command))  # noqa: S603


def update_poetry_dependencies(
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
        run_cmd_in_subprocess(
            f'"{python_executable}" -m poetry remove --lock{group_arg} {dependencies}'
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
        run_cmd_in_subprocess(poetry_add_cmd)

    # Run poetry update
    poetry_update_cmd = f'"{python_executable}" -m poetry update'
    if lock_only:
        poetry_update_cmd += " --lock"
    run_cmd_in_subprocess(poetry_update_cmd)

    # Fix the formatting of the pyproject.toml file
    python_script_location = Path(python_executable).parent
    run_cmd_in_subprocess(
        f'"{python_script_location}/toml-sort" '
        f'"{repository_root_directory}/pyproject.toml" --in-place --sort-table-keys'
    )


def get_pre_commit_repos(repository_root_directory: Path) -> list[str]:
    """Get the list of repo urls from the .pre-commit-config.yaml file.

    Args:
        repository_root_directory: The root directory of the repository.

    Returns:
        The list of repo urls.
    """
    pre_commit_file_data = yaml.safe_load(
        (repository_root_directory / ".pre-commit-config.yaml").read_text()
    )
    repo_list: list[str] = []
    for repo in pre_commit_file_data.get("repos", []):
        if (repo_url := str(repo["repo"])) == "local":
            continue  # skip local repos, they don't need to be updated
        repo_list.append(repo_url)
    return repo_list


def update_pre_commit_dependencies(
    python_executable: str,
    repository_root_directory: Path,
    pre_commit_repo_update_skip_list: list[str],
) -> None:
    """Update the pre-commit dependencies in the .pre-commit-config.yaml file.

    This function will also fix the formatting of the yaml file using the `yamlfix` package.

    Args:
        python_executable: The path to the python executable to use.
        repository_root_directory: The root directory of the repository.
        pre_commit_repo_update_skip_list: A list of pre-commit repo urls to skip updating.
    """
    run_cmd_in_subprocess(
        f"git config --global --add safe.directory "
        f'"{repository_root_directory.resolve().as_posix()}"'
    )
    # Update every hook in the pre-commit config file, skipping any hooks in the skip list
    for repo in get_pre_commit_repos(repository_root_directory):
        if repo in pre_commit_repo_update_skip_list:
            continue
        run_cmd_in_subprocess(
            f'"{python_executable}" -m pre_commit autoupdate --freeze --repo {repo}'
        )

    # Fix the formatting of the pre-commit config file
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        fix_files([f"{repository_root_directory}/.pre-commit-config.yaml"])


def sort_requirements_file(file_path: Path) -> None:
    """Sort the lines in the given requirements file.

    Args:
        file_path: The path to the requirements file to sort.
    """
    with file_path.open() as file:
        lines = sorted(file.readlines(), key=lambda x: x.lower().split("==")[0])
    with file_path.open("w") as file:
        file.writelines(lines)


def export_requirements_files(python_executable: str, dependency_groups: list[str]) -> None:
    """Export the requirements files for the specified dependency groups.

    This function uses the `poetry export` command to generate the requirements files for the
    specified dependency groups.

    Args:
        python_executable: The path to the python executable to use.
        dependency_groups: The list of dependency groups to export the requirements for.
    """
    run_cmd_in_subprocess(f'"{python_executable}" -m poetry config warnings.export false')

    for group_output_pair in dependency_groups:
        if ":" in group_output_pair:
            group, output_folder = group_output_pair.split(":", maxsplit=1)
        else:
            group = group_output_pair
            output_folder = group
        run_cmd_in_subprocess(
            f'"{python_executable}" -m poetry export --only {group} '
            f"--without-hashes --output {output_folder}/requirements.txt"
        )
        sort_requirements_file(Path(f"{output_folder}/requirements.txt"))


def main() -> None:
    """Run the script to update the development dependencies."""
    # Load in the GitHub Action inputs
    # See https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#example-specifying-inputs
    repo_root = os.environ["INPUT_REPO-ROOT"]
    dependency_dict = convert_dict_input(os.environ["INPUT_DEPENDENCY-DICT"])
    export_dependency_groups = [
        x.strip() for x in os.environ["INPUT_EXPORT-DEPENDENCY-GROUPS"].split(",") if x
    ]
    pre_commit_hook_run_skip_list = os.environ["INPUT_PRE-COMMIT-HOOK-SKIP-LIST"]
    pre_commit_repo_update_skip_list = [
        x.strip() for x in os.environ["INPUT_PRE-COMMIT-REPO-UPDATE-SKIP-LIST"].split(",") if x
    ]
    install_dependencies = os.environ["INPUT_INSTALL-DEPENDENCIES"].lower() in _ENV_VAR_TRUE_VALUES
    run_pre_commit = os.environ["INPUT_RUN-PRE-COMMIT"].lower() in _ENV_VAR_TRUE_VALUES
    update_pre_commit = os.environ["INPUT_UPDATE-PRE-COMMIT"].lower() in _ENV_VAR_TRUE_VALUES
    python_executable = sys.executable

    repo_root_path = Path(repo_root).resolve()
    os.chdir(repo_root_path)
    print(f"\nUpdating development dependencies in {Path.cwd()}")

    update_poetry_dependencies(
        python_executable, repo_root_path, dependency_dict, lock_only=not install_dependencies
    )
    if update_pre_commit or run_pre_commit:
        update_pre_commit_dependencies(
            python_executable, repo_root_path, pre_commit_repo_update_skip_list
        )
    if export_dependency_groups:
        export_requirements_files(python_executable, export_dependency_groups)
    if run_pre_commit:
        # Run the pre-commit hooks, ignore any errors since they are
        # just being run to auto-fix files.
        with contextlib.suppress(subprocess.CalledProcessError):
            os.environ["SKIP"] = pre_commit_hook_run_skip_list
            run_cmd_in_subprocess(f'"{python_executable}" -m pre_commit run --all-files')


if __name__ == "__main__":  # pragma: no cover
    # Run the main function
    main()
