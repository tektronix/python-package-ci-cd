"""Provide pytest fixtures and other configuration for testing."""

from pathlib import Path

import pytest


@pytest.fixture(name="mock_github_output_file")
def fixture_mock_github_output_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Mock the GitHub output file.

    Args:
        tmp_path (fixture): The temporary path fixture.
        monkeypatch (fixture): The monkeypatch fixture.
    """
    github_output_file = tmp_path / "github_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(github_output_file))
    return github_output_file
