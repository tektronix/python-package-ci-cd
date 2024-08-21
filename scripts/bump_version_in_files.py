"""This script will bump the version of the GitHub Actions to the newest version.

This script is intended to be run as a part of the release process in the `python-semantic-release`
`build-command`.
"""

from __future__ import annotations

import os
import re

from pathlib import Path

DIRECTORIES_TO_SEARCH = [".github", "workflows", "actions"]
FILES_TO_UPDATE = [Path("README.md")]
GITHUB_WORKFLOW_AND_ACTION_REGEX = re.compile(
    r"(uses: tektronix/python-package-ci-cd/.*?)@v\d+\.\d+\.\d+"
)


def get_file_paths(directory_list: list[str]) -> list[Path]:
    """Get a list of file paths from the given directories.

    Args:
        directory_list: A list of directories to search for files in.
    """
    file_paths: list[Path] = []
    for directory in directory_list:
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                file_paths.append(Path(dirpath) / Path(filename))  # noqa: PERF401
    return file_paths


def update_github_actions_version(filepath: Path, incoming_version: str) -> None:
    """Update the version of the GitHub Actions to the incoming version.

    Args:
        filepath: The path to the file to update.
        incoming_version: The version to update the file to
    """
    file_content = filepath.read_text()
    # Check if there's a match before replacing
    if GITHUB_WORKFLOW_AND_ACTION_REGEX.search(file_content):
        # Replace the version numbers with the new version
        updated_content = GITHUB_WORKFLOW_AND_ACTION_REGEX.sub(
            rf"\1@v{incoming_version}", file_content
        )
        print(f'Bumping version in "{filepath}" to', incoming_version)
        filepath.write_text(updated_content)
    else:
        print(f'No GitHub Workflow/Action usage found in "{filepath}", skipping update.')


if __name__ == "__main__":
    if not (new_version := os.getenv("NEW_VERSION")):
        msg = "NEW_VERSION environment variable is not set"
        raise SystemExit(msg)

    for file_path in get_file_paths(DIRECTORIES_TO_SEARCH) + FILES_TO_UPDATE:
        update_github_actions_version(file_path, new_version)
