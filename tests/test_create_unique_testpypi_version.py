"""Test the create_unique_testpypi_version action Python code."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

import actions.create_unique_testpypi_version.main

from actions.create_unique_testpypi_version.main import create_new_post_version, main

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

# Sample data for mocking
PACKAGE_NAME = "example-package"
CURRENT_VERSION = "0.1.0"
LATEST_VERSION = "0.1.0.post1"
NEW_VERSION = "0.1.0.post2"


@pytest.fixture(autouse=True)
def _mock_environment(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    """Mock the environment variables.

    Args:
        monkeypatch (fixture): The monkeypatch fixture.
    """
    # Mock environment variables
    monkeypatch.setenv("INPUT_PACKAGE-NAME", PACKAGE_NAME)


@pytest.fixture(name="mock_testpypi_server")
def fixture_mock_testpypi_server() -> Generator[MagicMock]:
    """Mock the PyPISimple class and its methods."""
    with patch("actions.create_unique_testpypi_version.main.PyPISimple") as mock_pypi_simple:
        mock_server = mock_pypi_simple.return_value
        mock_project_page = MagicMock()
        mock_project_page.packages = [MagicMock(version=LATEST_VERSION)]
        mock_server.get_project_page.return_value = mock_project_page
        yield mock_server


@pytest.fixture(name="mock_pyproject_file")
def fixture_mock_pyproject_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Mock the pyproject.toml file.

    Args:
        tmp_path (fixture): The temporary path fixture.
        monkeypatch (fixture): The monkeypatch fixture.
    """
    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(f"""
    [tool.poetry]
    name = "{PACKAGE_NAME}"
    version = "{CURRENT_VERSION}"
    """)
    monkeypatch.setattr(
        actions.create_unique_testpypi_version.main, "PYPROJECT_FILE", pyproject_file
    )
    return pyproject_file


def test_main(
    mock_testpypi_server: MagicMock,  # noqa: ARG001
    mock_pyproject_file: Path,
    mock_github_output_file: Path,
) -> None:
    """Test the main function.

    Args:
        mock_testpypi_server (fixture): Mock the PyPISimple class and its methods.
        mock_pyproject_file (fixture): Mock the pyproject.toml file.
        mock_github_output_file (fixture): Mock the GitHub output file.
    """
    main()

    # Check the pyproject.toml file for the updated version
    with mock_pyproject_file.open("r") as f:
        data = f.read()
        assert f'version = "{NEW_VERSION}"' in data

    # Check the GitHub output file for the new version variable
    with mock_github_output_file.open("r") as f:
        data = f.read()
        assert f"new-version={NEW_VERSION}\n" in data


@pytest.mark.parametrize(
    ("package_name", "latest_version", "local_version", "expected_version"),
    [
        ("example-package", "1.0.0", "0.1.0", "1.0.0.post1"),
        ("example-package", "1.0.0.post10", "0.1.0", "1.0.0.post11"),
        ("example-package", None, "0.1.0", "0.1.0.post1"),
        ("example-package", "0.1.0.post3", "0.1.0", "0.1.0.post4"),
        ("example-package", "2.3.4", "2.3.4", "2.3.4.post1"),
        ("example-package", None, "2.3.4.post5", "2.3.4.post6"),
    ],
)
def test_create_new_post_version(
    package_name: str, latest_version: str | None, local_version: str, expected_version: str
) -> None:
    """Test the create_new_post_version function.

    Args:
        package_name: The name of the package.
        latest_version: The latest version of the package.
        local_version: The local version of the package.
        expected_version: The expected new version of the package.
    """
    result = create_new_post_version(package_name, latest_version, local_version)
    assert result == expected_version
