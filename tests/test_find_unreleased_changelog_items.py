"""Test the find_unreleased_changelog_items action Python code."""

from __future__ import annotations

from pathlib import Path

import pytest

from actions.find_unreleased_changelog_items.main import find_template_folder, main

PREVIOUS_CHANGELOG_FILENAME = "previous_changelog.md"
PREVIOUS_RELEASE_NOTES_FILENAME = "previous_release_notes.md"
MOCK_TEMPLATES_FOLDER = "mock_templates"


@pytest.fixture()
def mock_pyproject_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> tuple[Path, Path]:
    """Mock the pyproject.toml file.

    Args:
        monkeypatch: The monkeypatch fixture.
        tmp_path: The temporary path fixture.

    Returns:
        The path to the pyproject.toml file and the path to the template folder.
    """
    pyproject_content = f"""
    [tool.semantic_release.changelog]
    template_dir = "{MOCK_TEMPLATES_FOLDER}"
    """
    mock_path = tmp_path / "pyproject.toml"
    mock_path.write_text(pyproject_content)
    monkeypatch.setattr("actions.find_unreleased_changelog_items.main.PYPROJECT_FILE", mock_path)
    template_folder = tmp_path / MOCK_TEMPLATES_FOLDER
    template_folder.mkdir()
    return mock_path, template_folder


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
def mock_env_vars(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, summary_file: Path) -> None:
    """Mock the environment variables to simulate GitHub Actions inputs.

    Args:
        tmp_path: The temporary path fixture.
        monkeypatch: The monkeypatch fixture.
        summary_file: The path to the job summary file.
    """
    # Change the working directory
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("INPUT_PREVIOUS-CHANGELOG-FILENAME", PREVIOUS_CHANGELOG_FILENAME)
    monkeypatch.setenv("INPUT_PREVIOUS-RELEASE-NOTES-FILENAME", PREVIOUS_RELEASE_NOTES_FILENAME)
    monkeypatch.setenv("INPUT_RELEASE-LEVEL", "minor")
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary_file))


@pytest.mark.parametrize(
    ("pyproject_content", "expected_template_folder"),
    [
        (
            '[tool.semantic_release.changelog]\ntemplate_dir = "mock_templates"\n',
            Path("mock_templates"),
        ),
        (
            "[tool.semantic_release.changelog]\n",
            Path("templates"),
        ),
    ],
)
def test_find_template_folder(
    mock_pyproject_file: tuple[Path, Path], pyproject_content: str, expected_template_folder: Path
) -> None:
    """Test the find_template_folder function.

    Args:
        mock_pyproject_file: Mock the pyproject.toml file.
        pyproject_content: The content to write to the pyproject.toml file.
        expected_template_folder: The expected template folder path.
    """
    mock_pyproject_file[0].write_text(pyproject_content)
    template_folder = find_template_folder()
    assert template_folder == expected_template_folder


def test_main_no_unreleased_entries(
    mock_env_vars: None,  # noqa: ARG001
    mock_changelog_file: Path,
    summary_file: Path,  # noqa: ARG001
    mock_pyproject_file: Path,  # noqa: ARG001
) -> None:
    """Test the main function when no unreleased entries are found.

    Args:
        mock_env_vars: Mock the environment variables.
        mock_changelog_file: Mock the changelog file.
        summary_file: Mock the environment variables.
        mock_pyproject_file: Mock the pyproject.toml file.
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
    mock_pyproject_file: tuple[Path, Path],
    mock_changelog_file: Path,
    summary_file: Path,
) -> None:
    """Test the main function when unreleased entries are found.

    Args:
        mock_env_vars: Mock the environment variables.
        mock_pyproject_file: Mock the pyproject.toml file.
        mock_changelog_file: Mock the changelog file.
        summary_file: Mock the environment variables.
    """
    _, template_folder = mock_pyproject_file
    template_changelog_file = template_folder / PREVIOUS_CHANGELOG_FILENAME
    template_release_notes_file = template_folder / PREVIOUS_RELEASE_NOTES_FILENAME
    main()

    assert template_changelog_file.read_text() == mock_changelog_file.read_text()
    assert (
        template_release_notes_file.read_text().strip() == "## Unreleased\n### Added\n- New feature"
    )

    with summary_file.open("r") as summary_file_handle:
        summary_contents = summary_file_handle.read()
    assert "## Workflow Inputs\n- release-level: minor\n" in summary_contents
    assert "## Incoming Changes\n### Added\n- New feature" in summary_contents


def test_main_with_no_release_level(
    mock_env_vars: None,  # noqa: ARG001
    mock_pyproject_file: tuple[Path, Path],
    mock_changelog_file: Path,
    summary_file: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the main function when unreleased entries are found but no release_level is provided.

    Args:
        mock_env_vars: Mock the environment variables.
        mock_pyproject_file: Mock the pyproject.toml file.
        mock_changelog_file: Mock the changelog file.
        summary_file: Mock the environment variables.
        monkeypatch: The monkeypatch fixture.
    """
    _, template_folder = mock_pyproject_file
    template_changelog_file = template_folder / PREVIOUS_CHANGELOG_FILENAME
    template_release_notes_file = template_folder / PREVIOUS_RELEASE_NOTES_FILENAME

    # Unset the INPUT_RELEASE-LEVEL environment variable
    monkeypatch.delenv("INPUT_RELEASE-LEVEL", raising=False)
    main()

    assert template_changelog_file.read_text() == mock_changelog_file.read_text()
    assert (
        template_release_notes_file.read_text().strip() == "## Unreleased\n### Added\n- New feature"
    )
    assert not summary_file.exists()
