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
import shutil

CHANGELOG_FILE = pathlib.Path("./CHANGELOG.md")


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

    # Copy the files to the correct location
    shutil.copy(CHANGELOG_FILE, template_changelog_filepath)
    with template_release_notes_filepath.open("w", encoding="utf-8") as template_release_notes:
        template_release_notes.write(release_notes_content.strip() + "\n")

    # If running in GitHub Actions, and the release_level is set, send the release level and
    # incoming changes to the GitHub Summary
    if release_level:
        summary_contents = (
            f"## Workflow Inputs\n- release-level: {release_level}\n"
            f"## Incoming Changes\n{release_notes_content.replace('## Unreleased', '').strip()}\n"
        )
        print(
            f"Adding the following contents to the GitHub Workflow Summary:\n\n{summary_contents}"
        )
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary_file:  # noqa: PTH123
            summary_file.write(summary_contents)


if __name__ == "__main__":  # pragma: no cover
    # Run the main function
    main()
