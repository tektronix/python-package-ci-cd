"""This script will check for unreleased entries in the CHANGELOG.md file.

It will exit with a non-zero exit code if there are no unreleased entries.

This script will do a few things:
    - It will copy the necessary files into the defined template directory to properly update the
        CHANGELOG.md and render the GitHub Release Notes.
    - It can be configured to output the Unreleased changes and incoming version bump level into
        the GITHUB_STEP_SUMMARY for easy viewing on the Workflow build summary page.
"""

import argparse
import os
import pathlib
import re
import shutil
import sys

import tomli

_ENV_VAR_TRUE_VALUES = {"1", "true", "yes"}
RUNNING_IN_GITHUB_ACTIONS = bool(os.getenv("GITHUB_ACTION"))
PYPROJECT_FILE = pathlib.Path("./pyproject.toml")
CHANGELOG_FILEPATH = pathlib.Path("./CHANGELOG.md")


def _parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments.

    Returns:
        The parsed Namespace.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--previous-changelog",
        required=True,
        action="store",
        dest="previous_changelog",
        help=(
            "The name of the file to copy the contents of the changelog into for use "
            "in the `python-semantic-release` templates."
        ),
    )
    parser.add_argument(
        "--previous-release-notes",
        required=True,
        action="store",
        dest="previous_release_notes",
        help=(
            "The name of the file to copy the contents of the `## Unreleased` "
            "section of the changelog into for use in the GitHub Release Notes."
        ),
    )
    parser.add_argument(
        "--release-level",
        required=False,
        action="store",
        dest="release_level",
        help=(
            "Provide the incoming version bump level. If this is provided, the script will "
            "output the release level and the unreleased changes to the GITHUB_STEP_SUMMARY."
        ),
    )

    return parser.parse_args()


def _find_template_folder() -> pathlib.Path:
    """Find the template folder from the pyproject.toml file.

    Returns:
        The path to the template folder.
    """
    with PYPROJECT_FILE.open("rb") as file_handle:
        pyproject_data = tomli.load(file_handle)
    try:
        template_folder = pathlib.Path(
            pyproject_data["tool"]["semantic_release"]["changelog"]["template_dir"]
        )
    except KeyError:
        template_folder = pathlib.Path("./templates")
    return template_folder


def main() -> None:
    """Check for entries in the Unreleased section of the CHANGELOG.md file.

    Raises:
        SystemExit: Indicates no new entries were found.
    """
    args = _parse_arguments()

    # Set the filepaths for the template files
    template_folder = _find_template_folder()
    template_changelog_filepath = template_folder / args.previous_changelog
    template_release_notes_filepath = template_folder / args.previous_release_notes

    release_notes_content = ""
    found_entries = False
    with CHANGELOG_FILEPATH.open(mode="r", encoding="utf-8") as changelog_file:
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
        msg = f"No unreleased entries were found in {CHANGELOG_FILEPATH}."
        raise SystemExit(msg)

    # Copy the files to the correct location
    shutil.copy(CHANGELOG_FILEPATH, template_changelog_filepath)
    with template_release_notes_filepath.open("w", encoding="utf-8") as template_release_notes:
        template_release_notes.write(release_notes_content.strip() + "\n")

    # If running in GitHub Actions, and the release_level is set, send the release level and
    # incoming changes to the GitHub Summary
    if RUNNING_IN_GITHUB_ACTIONS and args.release_level:
        summary_contents = (
            f"## Workflow Inputs\n- release-level: {args.release_level}\n"
            f"## Incoming Changes\n{release_notes_content.replace('## Unreleased', '').strip()}\n"
        )
        print(
            f"Adding the following contents to the GitHub Workflow Summary:\n\n{summary_contents}"
        )
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary_file:  # noqa: PTH123
            summary_file.write(summary_contents)


if __name__ == "__main__":
    # Handle GitHub Actions environment variables
    # See https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables
    if RUNNING_IN_GITHUB_ACTIONS:
        sys.argv.extend(
            [
                "--previous-changelog",
                os.getenv("INPUT_PREVIOUS-CHANGELOG-FILENAME", ""),
                "--previous-release-notes",
                os.getenv("INPUT_PREVIOUS-RELEASE-NOTES-FILENAME", ""),
            ]
        )
        if release_level := os.getenv("INPUT_RELEASE-LEVEL"):
            sys.argv.extend(["--release-level", release_level])

    main()
