"""Test the find_unreleased_changelog_items action Python code."""

from __future__ import annotations

import re
import shlex
import subprocess

from typing import TYPE_CHECKING
from unittest import mock

import pytest

from actions.find_unreleased_changelog_items.main import get_commit_messages, get_latest_tag, main

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_subprocess import FakeProcess

PREVIOUS_CHANGELOG_FILEPATH = "previous_changelog.md"
PREVIOUS_RELEASE_NOTES_FILEPATH = "previous_release_notes.md"
MOCK_TEMPLATES_FOLDER = "mock_templates"


@pytest.fixture(name="mock_previous_files")
def fixture_mock_previous_files(tmp_path: Path) -> tuple[Path, Path]:
    """Create filepaths in the temporary directory for the template files.

    Args:
        tmp_path: The temporary path fixture.

    Returns:
        The path to the previous changelog file and previous release notes file.
    """
    template_folder = tmp_path / MOCK_TEMPLATES_FOLDER
    template_folder.mkdir()
    return (
        template_folder / PREVIOUS_CHANGELOG_FILEPATH,
        template_folder / PREVIOUS_RELEASE_NOTES_FILEPATH,
    )


@pytest.fixture(name="mock_changelog_file")
def fixture_mock_changelog_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Mock the pyproject.toml file.

    Args:
        monkeypatch: The monkeypatch fixture.
        tmp_path: The temporary path fixture.

    Returns:
        The path to the changelog file.
    """
    changelog_content = """# Changelog
---
## Unreleased
### Added
- New feature
"""
    mock_path = tmp_path / "CHANGELOG.md"
    mock_path.write_text(changelog_content)
    monkeypatch.setattr("actions.find_unreleased_changelog_items.main.CHANGELOG_FILE", mock_path)
    return mock_path


@pytest.fixture(name="summary_file")
def fixture_summary_file(tmp_path: Path) -> Path:
    """Create a summary file for the GitHub Actions step.

    Args:
        tmp_path: The temporary path fixture.

    Returns:
        The path to the job summary file.
    """
    return tmp_path / "github_summary.txt"


@pytest.fixture(name="mock_env_vars")
def fixture_mock_env_vars(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    summary_file: Path,
    mock_previous_files: tuple[Path, Path],
    fake_process: FakeProcess,
) -> None:
    """Mock the environment variables to simulate GitHub Actions inputs.

    This fixture also mocks subprocess.check_output to enable testing to function without running
    git commands.

    Args:
        tmp_path: The temporary path fixture.
        monkeypatch: The monkeypatch fixture.
        summary_file: The path to the job summary file.
        mock_previous_files: Paths to the previous changelog file and previous release notes file.
        fake_process: The fake_process fixture, used to register commands that will be mocked.
    """
    fake_process.register(  # pyright: ignore[reportUnknownMemberType]
        shlex.split(f"git config --global --add safe.directory {tmp_path.resolve().as_posix()}")
    )
    fake_process.register(shlex.split("git describe --tags --abbrev=0"), stdout=b"v1.0.0\n")  # pyright: ignore[reportUnknownMemberType]
    fake_process.register(  # pyright: ignore[reportUnknownMemberType]
        shlex.split("git log v1.0.0..HEAD --pretty=format:%s"),
        stdout=b"Initial commit\nAdd new feature (#123)\n",
    )
    # Change the working directory
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("INPUT_PREVIOUS-CHANGELOG-FILEPATH", mock_previous_files[0].as_posix())
    monkeypatch.setenv("INPUT_PREVIOUS-RELEASE-NOTES-FILEPATH", mock_previous_files[1].as_posix())
    monkeypatch.setenv("INPUT_RELEASE-LEVEL", "minor")
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary_file))


def test_main_no_unreleased_entries(
    mock_env_vars: None,  # noqa: ARG001
    mock_changelog_file: Path,
    summary_file: Path,  # noqa: ARG001
    mock_github_output_file: Path,  # noqa: ARG001
) -> None:
    """Test the main function when no unreleased entries are found.

    Args:
        mock_env_vars: Mock the environment variables.
        mock_changelog_file: Mock the changelog file.
        summary_file: Mock the environment variables.
        mock_github_output_file (fixture): Mock the GitHub output file.
    """
    # Modify the changelog content to have no unreleased entries
    changelog_content = """# Changelog
---
## Released
### Added
- Released feature
"""
    mock_changelog_file.write_text(changelog_content)

    with pytest.raises(SystemExit, match=r"No unreleased entries were found in.*"):
        main()


def test_main_with_no_merged_prs(
    mock_env_vars: None,  # noqa: ARG001
    mock_changelog_file: Path,  # noqa: ARG001
    fake_process: FakeProcess,
    mock_github_output_file: Path,
) -> None:
    """Test the main function when unreleased entries are found.

    Args:
        mock_env_vars: Mock the environment variables.
        mock_changelog_file: Mock the changelog file.
        fake_process: The fake_process fixture, used to register commands that will be mocked.
        mock_github_output_file (fixture): Mock the GitHub output file.
    """
    fake_process.register(  # pyright: ignore[reportUnknownMemberType]
        shlex.split("git log v1.0.0..HEAD --pretty=format:%s"),
        stdout=b"Initial commit\n",
    )
    with fake_process.context() as nested_process:
        nested_process.register(  # pyright: ignore[reportUnknownMemberType]
            shlex.split("git log v1.0.0..HEAD --pretty=format:%s"),
            stdout=b"Initial commit\n",
        )
        with pytest.raises(
            SystemExit,
            match=re.escape("Issues found: ['No PRs have been merged since the last release']"),
        ):
            main()

    with mock_github_output_file.open("r") as f:
        data = f.read()
        assert "found-changes=false\n" in data


def test_main_with_unreleased_entries(
    mock_env_vars: None,  # noqa: ARG001
    mock_changelog_file: Path,
    summary_file: Path,
    mock_previous_files: tuple[Path, Path],
    mock_github_output_file: Path,
) -> None:
    """Test the main function when unreleased entries are found.

    Args:
        mock_env_vars: Mock the environment variables.
        mock_changelog_file: Mock the changelog file.
        summary_file: Mock the environment variables.
        mock_previous_files: Paths to the previous changelog file and previous release notes file.
        mock_github_output_file (fixture): Mock the GitHub output file.
    """
    main()

    assert mock_previous_files[0].read_text() == mock_changelog_file.read_text()
    assert mock_previous_files[1].read_text().strip() == "## Unreleased\n### Added\n- New feature"

    with summary_file.open("r") as summary_file_handle:
        summary_contents = summary_file_handle.read()
    assert (
        summary_contents
        == """## Workflow Inputs
- release-level: minor
## PRs Merged Since Last Release
- Add new feature (#123)
## Incoming Changes
### Added
- New feature
"""
    )

    with mock_github_output_file.open("r") as f:
        data = f.read()
        assert "found-changes=true\n" in data


def test_main_with_no_release_level(  # pylint: disable=too-many-positional-arguments
    mock_env_vars: None,  # noqa: ARG001
    mock_changelog_file: Path,
    summary_file: Path,
    mock_previous_files: tuple[Path, Path],
    monkeypatch: pytest.MonkeyPatch,
    mock_github_output_file: Path,  # noqa: ARG001
) -> None:
    """Test the main function when unreleased entries are found but no release_level is provided.

    Args:
        mock_env_vars: Mock the environment variables.
        mock_changelog_file: Mock the changelog file.
        summary_file: Mock the environment variables.
        mock_previous_files: Paths to the previous changelog file and previous release notes file.
        monkeypatch: The monkeypatch fixture.
        mock_github_output_file (fixture): Mock the GitHub output file.
    """
    # Unset the INPUT_RELEASE-LEVEL environment variable
    monkeypatch.delenv("INPUT_RELEASE-LEVEL", raising=False)
    main()

    assert mock_previous_files[0].read_text() == mock_changelog_file.read_text()
    assert mock_previous_files[1].read_text().strip() == "## Unreleased\n### Added\n- New feature"
    assert not summary_file.exists()


def test_get_latest_tag() -> None:
    """Test the get_latest_tag function."""
    with mock.patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = b"v1.0.0\n"
        assert get_latest_tag() == "v1.0.0"

        mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")
        assert get_latest_tag() is None


def test_get_commit_messages() -> None:
    """Test the get_commit_messages function."""
    with mock.patch("subprocess.check_output") as mock_check_output:
        mock_check_output.return_value = b"Initial commit\nAdd new feature\n"
        assert get_commit_messages() == ["Initial commit", "Add new feature"]
