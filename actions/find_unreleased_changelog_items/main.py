"""This script will check for unreleased entries in the CHANGELOG.md file.

It will exit with a non-zero exit code if there are no unreleased entries.

This script needs to be run from a directory that contains a `pyproject.toml` file and a
`CHANGELOG.md` file.

This script will do a few things:
    - It will copy the necessary files into the defined template directory to properly update the
        CHANGELOG.md and render the GitHub Release Notes.
    - It can be configured to output the Unreleased changes and incoming version bump level into
        the GITHUB_STEP_SUMMARY for easy viewing on the Workflow build summary page.
"""

from __future__ import annotations

import os
import pathlib
import re
import shlex
import shutil
import subprocess

CHANGELOG_FILE = pathlib.Path("./CHANGELOG.md")


def run_cmd_in_subprocess(command: str) -> str:
    """Run the given command in a subprocess and return the result.

    Args:
        command: The command string to send.

    Returns:
        The output from the command.
    """
    command = command.replace("\\", "/")
    print(f"\nExecuting command: {command}")
    return subprocess.check_output(shlex.split(command)).decode()  # noqa: S603


def get_latest_tag() -> str | None:
    """Retrieve the latest tag in the Git repository.

    Returns:
        The latest tag as a string if it exists, otherwise None.
    """
    try:
        return run_cmd_in_subprocess("git describe --tags --abbrev=0").strip()
    except subprocess.CalledProcessError:
        return None


def get_commit_messages(since_tag: str | None = None) -> list[str]:
    """Retrieve commit messages from the Git repository.

    Args:
        since_tag: The tag from which to start listing commits. If None, lists all commits.

    Returns:
        A list of commit messages as strings.
    """
    range_spec = f"{since_tag}..HEAD" if since_tag else "HEAD"
    return run_cmd_in_subprocess(f"git log {range_spec} --pretty=format:%s").splitlines()


def add_contents_to_github_summary(contents: str) -> None:
    """Add the given contents to the GitHub Workflow Summary.

    Args:
        contents: The contents to add to the summary.
    """
    print(f"\nAdding the following contents to the GitHub Workflow Summary:\n\n{contents}")
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary_file:  # noqa: PTH123
        summary_file.write(contents)


def parse_changelog_file(changelog_filepath: pathlib.Path) -> tuple[bool, str]:
    """Parse the changelog file and return the release notes and unreleased content.

    Args:
        changelog_filepath: The path to the changelog file.

    Returns:
        A tuple with a boolean indicating if any entries were found and the release notes content.
    """
    release_notes_content = ""
    found_entries = False
    with changelog_filepath.open(mode="r", encoding="utf-8") as changelog_file:
        tracking_unreleased = False
        tracking_entries = False
        for line in changelog_file:
            if line.startswith(("___", "---")):
                tracking_unreleased = False
                tracking_entries = False
            if line.startswith("## Unreleased"):
                tracking_unreleased = True
            if tracking_unreleased:
                release_notes_content += line
            if tracking_unreleased and line.startswith(
                (
                    "### Added\n",
                    "### Changed\n",
                    "### Deprecated\n",
                    "### Removed\n",
                    "### Fixed\n",
                    "### Security\n",
                )
            ):
                tracking_entries = True
            if tracking_entries and not found_entries:
                found_entries = bool(re.match(r"^- \w+", line))

    return found_entries, release_notes_content


def main() -> None:
    """Check for entries in the Unreleased section of the CHANGELOG.md file.

    Raises:
        SystemExit: Indicates no new entries were found.
    """
    # Load in the GitHub Action inputs
    # See https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#example-specifying-inputs
    filepath_for_previous_changelog = os.environ["INPUT_PREVIOUS-CHANGELOG-FILEPATH"]
    filepath_for_previous_release_notes = os.environ["INPUT_PREVIOUS-RELEASE-NOTES-FILEPATH"]
    release_level = os.getenv("INPUT_RELEASE-LEVEL")
    # Set the filepaths for the template files
    template_changelog_filepath = pathlib.Path(filepath_for_previous_changelog)
    template_release_notes_filepath = pathlib.Path(filepath_for_previous_release_notes)
    root_dir = pathlib.Path.cwd()

    found_entries, release_notes_content = parse_changelog_file(CHANGELOG_FILE)

    issue_messages: list[str] = []
    if not found_entries:
        issue_messages.append(f"No unreleased entries were found in {CHANGELOG_FILE}")

    # Check for merged PRs since the last release
    run_cmd_in_subprocess(
        f'git config --global --add safe.directory "{root_dir.resolve().as_posix()}"'
    )
    commit_messages = get_commit_messages(since_tag=get_latest_tag())
    pr_regex = re.compile(r"\(#\d+\)$")
    pr_descriptions = "\n".join([f"- {msg}" for msg in commit_messages if pr_regex.search(msg)])
    if not pr_descriptions and not os.getenv("UNIT_TESTING_FIND_UNRELEASED_CHANGELOG_ITEMS_ACTION"):
        issue_messages.append("No PRs have been merged since the last release")

    # Copy the files to the correct location
    shutil.copy(CHANGELOG_FILE, template_changelog_filepath)
    with template_release_notes_filepath.open("w", encoding="utf-8") as template_release_notes:
        template_release_notes.write(release_notes_content.strip() + "\n")

    if issue_messages:
        add_contents_to_github_summary(
            "## Status\nNo release activities will be performed as a part of this build\n"
            f"## Encountered Issues\n{''.join([f'- {msg}\n' for msg in issue_messages])}"
        )
    # If running in GitHub Actions, and the release_level is set, send the release level and
    # incoming changes to the GitHub Summary
    elif release_level:
        add_contents_to_github_summary(
            f"## Workflow Inputs\n- release-level: {release_level}\n"
            f"## PRs Merged Since Last Release\n{pr_descriptions}\n"
            f"## Incoming Changes\n{release_notes_content.replace('## Unreleased', '').strip()}\n"
        )

    # Set the output variable for GitHub Actions
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as github_output_file_handle:  # noqa: PTH123
        github_output_file_handle.write(f"found-changes={not issue_messages}\n".lower())

    # Raise an error if an issue was encountered
    if issue_messages:
        msg = f"Issues found: {issue_messages}"
        raise SystemExit(msg)


if __name__ == "__main__":  # pragma: no cover
    # Run the main function
    main()
