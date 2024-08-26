"""Test the find_unreleased_changelog_items action Python code."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from actions.find_unreleased_changelog_items.main import main

if TYPE_CHECKING:
    from pathlib import Path

PREVIOUS_CHANGELOG_FILEPATH = "previous_changelog.md"
PREVIOUS_RELEASE_NOTES_FILEPATH = "previous_release_notes.md"
MOCK_TEMPLATES_FOLDER = "mock_templates"


@pytest.fixture()
def mock_previous_files(tmp_path: Path) -> tuple[Path, Path]:
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


@pytest.fixture()
def mock_changelog_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
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


@pytest.fixture()
def summary_file(tmp_path: Path) -> Path:
    """Create a summary file for the GitHub Actions step.

    Args:
        tmp_path: The temporary path fixture.

    Returns:
        The path to the job summary file.
    """
    return tmp_path / "github_summary.txt"


@pytest.fixture()
def mock_env_vars(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    summary_file: Path,
    mock_previous_files: tuple[Path, Path],
) -> None:
    """Mock the environment variables to simulate GitHub Actions inputs.

    Args:
        tmp_path: The temporary path fixture.
        monkeypatch: The monkeypatch fixture.
        summary_file: The path to the job summary file.
        mock_previous_files: Paths to the previous changelog file and previous release notes file.
    """
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
) -> None:
    """Test the main function when no unreleased entries are found.

    Args:
        mock_env_vars: Mock the environment variables.
        mock_changelog_file: Mock the changelog file.
        summary_file: Mock the environment variables.
    """
    # Modify the changelog content to have no unreleased entries
    changelog_content = """# Changelog
---
## Released
### Added
- Released feature
"""
    mock_changelog_file.write_text(changelog_content)

    with pytest.raises(SystemExit, match="No unreleased entries were found in.*"):
        main()


def test_main_with_unreleased_entries(
    mock_env_vars: None,  # noqa: ARG001
    mock_changelog_file: Path,
    summary_file: Path,
    mock_previous_files: tuple[Path, Path],
) -> None:
    """Test the main function when unreleased entries are found.

    Args:
        mock_env_vars: Mock the environment variables.
        mock_changelog_file: Mock the changelog file.
        summary_file: Mock the environment variables.
        mock_previous_files: Paths to the previous changelog file and previous release notes file.
    """
    main()

    assert mock_previous_files[0].read_text() == mock_changelog_file.read_text()
    assert mock_previous_files[1].read_text().strip() == "## Unreleased\n### Added\n- New feature"

    with summary_file.open("r") as summary_file_handle:
        summary_contents = summary_file_handle.read()
    assert "## Workflow Inputs\n- release-level: minor\n" in summary_contents
    assert "## Incoming Changes\n### Added\n- New feature" in summary_contents


def test_main_with_no_release_level(
    mock_env_vars: None,  # noqa: ARG001
    mock_changelog_file: Path,
    summary_file: Path,
    mock_previous_files: tuple[Path, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the main function when unreleased entries are found but no release_level is provided.

    Args:
        mock_env_vars: Mock the environment variables.
        mock_changelog_file: Mock the changelog file.
        summary_file: Mock the environment variables.
        mock_previous_files: Paths to the previous changelog file and previous release notes file.
        monkeypatch: The monkeypatch fixture.
    """
    # Unset the INPUT_RELEASE-LEVEL environment variable
    monkeypatch.delenv("INPUT_RELEASE-LEVEL", raising=False)
    main()

    assert mock_previous_files[0].read_text() == mock_changelog_file.read_text()
    assert mock_previous_files[1].read_text().strip() == "## Unreleased\n### Added\n- New feature"
    assert not summary_file.exists()
