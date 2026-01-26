"""Test the update_development_dependencies action Python code."""

import sys

from collections.abc import Generator
from pathlib import Path
from typing import Any
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
PRE_COMMIT_REPO_UPDATE_SKIP_LIST = [
    "https://github.com/executablebooks/mdformat",
    "https://github.com/Lucas-C/pre-commit-hooks",
    "https://github.com/PyCQA/docformatter",
]


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
    (repo_root_directory / ".pre-commit-config.yaml").write_text(
        """---
default_install_hook_types: [pre-commit, commit-msg]
default_stages: [pre-commit]
ci:
  autofix_prs: false
  autoupdate_schedule: weekly
  autoupdate_commit_msg: 'chore(pre-commit-deps): pre-commit autoupdate'
  skip:
    - check-poetry
    - pylint
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: cef0300fd0fc4d2a87a85fa2093c6b283ea36f4b  # frozen: v5.0.0
    hooks:
      - id: check-yaml
        args: [--unsafe]
      - id: check-toml
      - id: check-json
      - id: check-xml
      - id: file-contents-sorter
        files: ^(doc_config/known_words.txt)$
        args: [--unique, --ignore-case]
      - id: requirements-txt-fixer
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: check-added-large-files
        args: [--maxkb=3000, --enforce-all]
      - id: forbid-submodules
      - id: pretty-format-json
        args: [--autofix, --indent=4]
  - repo: https://github.com/Lucas-C/pre-commit-hooks
    rev: a30f0d816e5062a67d87c8de753cfe499672b959  # frozen: v1.5.5
    hooks:
      - id: remove-tabs
      - id: forbid-tabs
  - repo: https://github.com/Mateusz-Grzelinski/actionlint-py
    rev: 27445053da613c660ed5895d9616662059a53ca7  # frozen: v1.7.3.17
    hooks:
      - id: actionlint
        additional_dependencies: [pyflakes, shellcheck-py]
  - repo: https://github.com/lyz-code/yamlfix
    rev: 8072181c0f2eab9f2dd8db2eb3b9556d7cd0bd74  # frozen: 1.17.0
    hooks:
      - id: yamlfix
  - repo: https://github.com/AleksaC/hadolint-py
    rev: e70baeefd566058716df2f29eae8fe8ffc213a9f  # frozen: v2.12.1b3
    hooks:
      - id: hadolint
        args: [--ignore=DL3008, --ignore=DL3018]
  - repo: https://github.com/executablebooks/mdformat
    rev: 86542e37a3a40974eb812b16b076220fe9bb4278  # frozen: 0.7.18
    hooks:
      - id: mdformat
        args: [--number, --end-of-line, keep]
        additional_dependencies:
          - mdformat-admon
          - mdformat-beautysh
  - repo: local
    hooks:
      - id: pylint
        name: pylint
        entry: pylint
        language: system
        types: [python]
        pass_filenames: true
        args: [-sn]
      - id: pyright
        name: pyright
        entry: pyright
        language: system
        types: [python]
        pass_filenames: false
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: 8983acb92ee4b01924893632cf90af926fa608f0  # frozen: v0.7.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  # TODO: Re-enable this once https://github.com/PyCQA/docformatter/issues/293 is resolved
  #  - repo: https://github.com/PyCQA/docformatter
  #    rev: dfefe062799848234b4cd60b04aa633c0608025e  # frozen: v1.7.5
  #    hooks:
  #      - id: docformatter
  #        additional_dependencies: [tomli]
"""
    )
    (repo_root_directory / "dev").mkdir()
    (repo_root_directory / "dev" / "requirements.txt").touch()

    monkeypatch.setenv("INPUT_REPO-ROOT", str(repo_root_directory))
    monkeypatch.setenv("INPUT_DEPENDENCY-DICT", '{"dev": ["pytest"]}')
    monkeypatch.setenv("INPUT_EXPORT-DEPENDENCY-GROUPS", "dev")
    monkeypatch.setenv(
        "INPUT_PRE-COMMIT-REPO-UPDATE-SKIP-LIST", ",".join(PRE_COMMIT_REPO_UPDATE_SKIP_LIST)
    )
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


def _create_mock_pre_commit_autoupdate_call(repo_url: str) -> Any:  # noqa: ANN401
    """Create a mock call for pre-commit autoupdate.

    Args:
        repo_url: The URL of the pre-commit repository.

    Returns:
        A call object representing the pre-commit autoupdate command.
    """
    return call(
        [
            PYTHON_EXECUTABLE,
            "-m",
            "pre_commit",
            "autoupdate",
            "--freeze",
            "--repo",
            repo_url,
        ]
    )


def test_update_pre_commit_dependencies(
    repo_root_dir: Path,
    monkeypatch: pytest.MonkeyPatch,  # noqa: ARG001
) -> None:
    """Test the update_pre_commit_dependencies function."""
    with patch("subprocess.check_call") as mock_subproc_call:
        update_pre_commit_dependencies(
            sys.executable, repo_root_dir, PRE_COMMIT_REPO_UPDATE_SKIP_LIST
        )

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
            _create_mock_pre_commit_autoupdate_call(
                "https://github.com/pre-commit/pre-commit-hooks"
            ),
            _create_mock_pre_commit_autoupdate_call(
                "https://github.com/Mateusz-Grzelinski/actionlint-py"
            ),
            _create_mock_pre_commit_autoupdate_call("https://github.com/lyz-code/yamlfix"),
            _create_mock_pre_commit_autoupdate_call("https://github.com/AleksaC/hadolint-py"),
            _create_mock_pre_commit_autoupdate_call("https://github.com/astral-sh/ruff-pre-commit"),
        ]
        assert mock_subproc_call.call_count == 6
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
        assert mock_subproc_call.call_count == 1
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
        assert mock_subproc_call.call_count == 12


def test_main_no_install_dependencies(
    repo_root_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the main function."""
    with (
        patch("subprocess.check_call") as mock_subproc_call,
        monkeypatch.context() as mocked_context,
    ):
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
