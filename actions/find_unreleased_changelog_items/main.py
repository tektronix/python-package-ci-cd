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

    release_notes_content = ""
    found_entries = False
    with CHANGELOG_FILE.open(mode="r", encoding="utf-8") as changelog_file:
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

    if not found_entries:
        msg = f"No unreleased entries were found in {CHANGELOG_FILE}."
        raise SystemExit(msg)

    # Check for merged PRs since the last release
    run_cmd_in_subprocess(
        f'git config --global --add safe.directory "{root_dir.resolve().as_posix()}"'
    )
    commit_messages = get_commit_messages(since_tag=get_latest_tag())
    pr_regex = re.compile(r"\(#\d+\)$")
    pr_descriptions = "\n".join([f"- {msg}" for msg in commit_messages if pr_regex.search(msg)])
    if not pr_descriptions and not os.getenv("UNIT_TESTING_FIND_UNRELEASED_CHANGELOG_ITEMS_ACTION"):
        msg = "No PRs have been merged since the last release."
        raise SystemExit(msg)

    # Copy the files to the correct location
    shutil.copy(CHANGELOG_FILE, template_changelog_filepath)
    with template_release_notes_filepath.open("w", encoding="utf-8") as template_release_notes:
        template_release_notes.write(release_notes_content.strip() + "\n")

    # If running in GitHub Actions, and the release_level is set, send the release level and
    # incoming changes to the GitHub Summary
    if release_level:
        summary_contents = (
            f"## Workflow Inputs\n- release-level: {release_level}\n"
            f"## PRs Merged Since Last Release\n{pr_descriptions}\n"
            f"## Incoming Changes\n{release_notes_content.replace('## Unreleased', '').strip()}\n"
        )
        print(
            f"\nAdding the following contents to the GitHub Workflow Summary:\n\n{summary_contents}"
        )
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary_file:  # noqa: PTH123
            summary_file.write(summary_contents)


if __name__ == "__main__":  # pragma: no cover
    # Run the main function
    main()
