"""Test the bump_version_in_files module."""

from pathlib import Path

import pytest

from scripts.bump_version_in_files import get_file_paths, update_github_actions_version


@pytest.fixture()
def temporary_directory(tmp_path: Path) -> Path:
    """Create a temporary directory."""
    # Create a temporary directory with some files
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "file1.txt").write_text("test")
    (test_dir / "file2.txt").write_text("test")
    (test_dir / "file3.txt").write_text("test")
    return test_dir


def test_get_file_paths(temporary_directory: Path) -> None:
    """Test the get_file_paths function."""
    path_list = get_file_paths([temporary_directory.as_posix()])
    assert len(path_list) == 3
    assert all(file_path.is_file() for file_path in path_list)


def test_update_github_actions_version_no_match(temporary_directory: Path) -> None:
    """Update version when no match is found."""
    file_path = temporary_directory / "file1.txt"
    file_path.write_text("no match here")
    update_github_actions_version(file_path, "1.2.3")
    assert file_path.read_text() == "no match here"


def test_update_github_actions_version_with_match(temporary_directory: Path) -> None:
    """Update version when a match is found."""
    file_path = temporary_directory / "file2.txt"
    file_path.write_text("uses: tektronix/python-package-ci-cd/some-action@v1.0.0")
    update_github_actions_version(file_path, "1.2.3")
    assert file_path.read_text() == "uses: tektronix/python-package-ci-cd/some-action@v1.2.3"


def test_update_github_actions_version_multiple_matches(temporary_directory: Path) -> None:
    """Update version when multiple matches are found."""
    file_path = temporary_directory / "file3.txt"
    file_path.write_text(
        "uses: tektronix/python-package-ci-cd/action1@v1.0.0\n"
        "uses: tektronix/python-package-ci-cd/action2@v2.0.0"
    )
    update_github_actions_version(file_path, "1.2.3")
    assert file_path.read_text() == (
        "uses: tektronix/python-package-ci-cd/action1@v1.2.3\n"
        "uses: tektronix/python-package-ci-cd/action2@v1.2.3"
    )