"""Test the update_development_dependencies action Python code."""

import sys

from collections.abc import Generator
from pathlib import Path
from unittest.mock import call, MagicMock, patch

import pytest

from actions.update_development_dependencies.main import (
    convert_dict_input,
    export_requirements_files,
    main,
    sort_requirements_file,
    update_poetry_dependencies,
    update_pre_commit_dependencies,
)

PYTHON_EXECUTABLE = Path(sys.executable).as_posix()


@pytest.fixture(autouse=True)
def mock_pypi_server() -> Generator[MagicMock]:
    """Mock the PyPISimple class and its methods."""
    with patch("actions.update_development_dependencies.main.PyPISimple") as mock_pypi_simple:
        mock_server = mock_pypi_simple.return_value
        mock_project_page = MagicMock()
        mock_project_page.packages = [MagicMock(version="1.0.0")]
        mock_server.get_project_page.return_value = mock_project_page
        yield mock_server


@pytest.fixture(name="repo_root_dir")
def fixture_repo_root_dir(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> Path:
    """Fixture to mock environment variables and repo root."""
    # Set up necessary files
    repo_root_directory = tmp_path / "repo"
    repo_root_directory.mkdir()
    monkeypatch.chdir(repo_root_directory)
    (repo_root_directory / ".pre-commit-config.yaml").touch()
    (repo_root_directory / "dev").mkdir()
    (repo_root_directory / "dev" / "requirements.txt").touch()

    monkeypatch.setenv("INPUT_REPO-ROOT", str(repo_root_directory))
    monkeypatch.setenv("INPUT_DEPENDENCY-DICT", '{"dev": ["pytest"]}')
    monkeypatch.setenv("INPUT_EXPORT-DEPENDENCY-GROUPS", "dev")
    monkeypatch.setenv("INPUT_PRE-COMMIT-HOOK-SKIP-LIST", "")
    monkeypatch.setenv("INPUT_INSTALL-DEPENDENCIES", "true")
    monkeypatch.setenv("INPUT_RUN-PRE-COMMIT", "true")
    monkeypatch.setenv("INPUT_UPDATE-PRE-COMMIT", "true")

    return repo_root_directory


def test_update_poetry_dependencies(
    repo_root_dir: Path,
    monkeypatch: pytest.MonkeyPatch,  # noqa: ARG001
) -> None:
    """Test the update_poetry_dependencies function."""
    with patch("subprocess.check_call") as mock_subproc_call:
        dependencies_to_update = {"dev": ["pytest"]}

        update_poetry_dependencies(
            PYTHON_EXECUTABLE, repo_root_dir, dependencies_to_update, lock_only=False
        )

        # Check the calls to subprocess.check_call
        expected_calls = [
            call([PYTHON_EXECUTABLE, "-m", "poetry", "remove", "--lock", "--group=dev", "pytest"]),
            call(
                [
                    PYTHON_EXECUTABLE,
                    "-m",
                    "poetry",
                    "add",
                    "--group=dev",
                    "pytest==1.0.0",
                ]
            ),
            call([PYTHON_EXECUTABLE, "-m", "poetry", "update"]),
            call(
                [
                    f"{Path(PYTHON_EXECUTABLE).parent.as_posix()}/toml-sort",
                    f"{repo_root_dir.as_posix()}/pyproject.toml",
                    "--in-place",
                    "--sort-table-keys",
                ]
            ),
        ]
        assert mock_subproc_call.call_count == 4
        mock_subproc_call.assert_has_calls(expected_calls, any_order=True)


def test_update_pre_commit_dependencies(
    repo_root_dir: Path,
    monkeypatch: pytest.MonkeyPatch,  # noqa: ARG001
) -> None:
    """Test the update_pre_commit_dependencies function."""
    with patch("subprocess.check_call") as mock_subproc_call:
        update_pre_commit_dependencies(sys.executable, repo_root_dir)

        # Check the calls to subprocess.check_call
        expected_calls = [
            call(
                [
                    "git",
                    "config",
                    "--global",
                    "--add",
                    "safe.directory",
                    f"{repo_root_dir.resolve().as_posix()}",
                ]
            ),
            call([PYTHON_EXECUTABLE, "-m", "pre_commit", "autoupdate", "--freeze"]),
        ]
        assert mock_subproc_call.call_count == 2
        mock_subproc_call.assert_has_calls(expected_calls, any_order=True)


def test_export_requirements_files(
    repo_root_dir: Path,
    monkeypatch: pytest.MonkeyPatch,  # noqa: ARG001
) -> None:
    """Test the export_requirements_files function."""
    with patch("subprocess.check_call") as mock_subproc_call:
        dependency_groups = ["dev:dev_output"]
        (repo_root_dir / "dev_output").mkdir()
        (repo_root_dir / "dev_output" / "requirements.txt").touch()

        export_requirements_files(PYTHON_EXECUTABLE, dependency_groups)

        # Check the calls to subprocess.check_call
        expected_calls = [
            call([PYTHON_EXECUTABLE, "-m", "poetry", "config", "warnings.export", "false"]),
            call(
                [
                    PYTHON_EXECUTABLE,
                    "-m",
                    "poetry",
                    "export",
                    "--only",
                    "dev",
                    "--without-hashes",
                    "--output",
                    "dev_output/requirements.txt",
                ]
            ),
        ]
        assert mock_subproc_call.call_count == 2
        mock_subproc_call.assert_has_calls(expected_calls, any_order=True)


def test_main(
    repo_root_dir: Path,  # noqa: ARG001
    monkeypatch: pytest.MonkeyPatch,  # noqa: ARG001
) -> None:
    """Test the main function."""
    with patch("subprocess.check_call") as mock_subproc_call:
        # Call the main function
        main()
        assert mock_subproc_call.called
        assert mock_subproc_call.call_count == 9


def test_main_no_install_dependencies(
    repo_root_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the main function."""
    with patch(
        "subprocess.check_call"
    ) as mock_subproc_call, monkeypatch.context() as mocked_context:
        mocked_context.setenv("INPUT_EXPORT-DEPENDENCY-GROUPS", "")
        mocked_context.setenv("INPUT_PRE-COMMIT-HOOK-SKIP-LIST", "")
        mocked_context.setenv("INPUT_INSTALL-DEPENDENCIES", "false")
        mocked_context.setenv("INPUT_RUN-PRE-COMMIT", "false")
        mocked_context.setenv("INPUT_UPDATE-PRE-COMMIT", "false")

        main()

        expected_calls = [
            call([PYTHON_EXECUTABLE, "-m", "poetry", "remove", "--lock", "--group=dev", "pytest"]),
            call(
                [
                    PYTHON_EXECUTABLE,
                    "-m",
                    "poetry",
                    "add",
                    "--group=dev",
                    "pytest==1.0.0",
                    "--lock",
                ]
            ),
            call([PYTHON_EXECUTABLE, "-m", "poetry", "update", "--lock"]),
            call(
                [
                    f"{Path(PYTHON_EXECUTABLE).parent.as_posix()}/toml-sort",
                    f"{repo_root_dir.as_posix()}/pyproject.toml",
                    "--in-place",
                    "--sort-table-keys",
                ]
            ),
        ]
        assert mock_subproc_call.call_count == 4
        mock_subproc_call.assert_has_calls(expected_calls, any_order=True)


def test_sort_requirements_file(tmp_path: Path) -> None:
    """Test the sort_requirements_file function."""
    # Create an unsorted requirements file
    unsorted_content = ["Flask==1.1.2\n", "requests==2.24.0\n", "pytest==6.0.1\n", "Django==3.1\n"]

    sorted_content = ["Django==3.1\n", "Flask==1.1.2\n", "pytest==6.0.1\n", "requests==2.24.0\n"]

    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text("".join(unsorted_content))

    # Call the function to sort the file
    sort_requirements_file(requirements_file)

    # Read the sorted file content
    sorted_file_content = requirements_file.read_text().splitlines(keepends=True)

    # Compare the sorted file content to the expected sorted content
    assert sorted_file_content == sorted_content


def test_convert_dict_input_valid() -> None:
    """Test convert_dict_input with valid input."""
    input_str = '{"dev": ["pytest", "mock"], "prod": ["django"]}'
    expected_output = {"dev": ["pytest", "mock"], "prod": ["django"]}
    assert convert_dict_input(input_str) == expected_output


def test_convert_dict_input_invalid_json() -> None:
    """Test convert_dict_input with invalid JSON input."""
    input_str = '{"dev": ["pytest", "mock", "prod": ["django"]}'
    with pytest.raises(
        ValueError,
        match=r'Input "{.*}" does not match the required type of `dict\[str, list\[str\]\]`.',
    ):
        convert_dict_input(input_str)


def test_convert_dict_input_invalid_structure() -> None:
    """Test convert_dict_input with invalid dictionary structure."""
    input_str = '{"dev": "pytest, mock", "prod": "django"}'
    with pytest.raises(
        ValueError,
        match=r'Input "{.*}" does not match the required type of `dict\[str, list\[str\]\]`.',
    ):
        convert_dict_input(input_str)


def test_convert_dict_input_non_string_keys() -> None:
    """Test convert_dict_input with non-string keys."""
    input_str = '{1: ["pytest", "mock"], "prod": ["django"]}'
    with pytest.raises(
        ValueError,
        match=r'Input "{.*}" does not match the required type of `dict\[str, list\[str\]\]`.',
    ):
        convert_dict_input(input_str)


def test_convert_dict_input_non_string_values() -> None:
    """Test convert_dict_input with non-string values."""
    input_str = '{"dev": ["pytest", 123], "prod": ["django"]}'
    with pytest.raises(
        ValueError,
        match=r'Input "{.*}" does not match the required type of `dict\[str, list\[str\]\]`.',
    ):
        convert_dict_input(input_str)


def test_convert_dict_input_empty_dict() -> None:
    """Test convert_dict_input with empty dictionary."""
    input_str = "{}"
    expected_output = {}
    assert convert_dict_input(input_str) == expected_output


def test_convert_dict_input_empty_lists() -> None:
    """Test convert_dict_input with empty lists."""
    input_str = '{"dev": [], "prod": []}'
    expected_output: dict[str, list[str]] = {"dev": [], "prod": []}
    assert convert_dict_input(input_str) == expected_output
