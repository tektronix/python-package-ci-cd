"""Create a unique post-release version for test.pypi.org.

This script will find the latest version of the package on test.pypi.org and create a new
post-release version, incrementing the `.postN` version if necessary. It will then write that
new version number back to the pyproject.toml file.

This script will also set the value of a GitHub Actions output variable named `new-version` to the
newly created version number.

This script needs to be run from a directory that contains a `pyproject.toml` file.
"""

from __future__ import annotations

import os
import pathlib

import tomli
import tomli_w

from poetry.core.constraints.version import Version
from pypi_simple import PyPISimple

PYPROJECT_FILE = pathlib.Path("./pyproject.toml")


def create_new_post_version(
    package_name: str, latest_version: str | None, local_version: str
) -> str:
    """Create a new `.postN` version, incrementing `N` if necessary.

    Args:
        package_name: The name of the package.
        latest_version: The current version of the package.
        local_version: The version of the package from the pyproject.toml file.

    Returns:
        The new `.postN` version as a string.
    """
    if latest_version:
        parsed_version = Version.parse(latest_version)
    else:
        parsed_version = Version.parse(local_version)

    print(f"Current version of `{package_name}` is: {parsed_version}")
    # Create the .postN version suffix
    new_post_release_num = 1
    if parsed_version.post:
        new_post_release_num += parsed_version.post.number

    # Create the new version number
    updated_version = Version.parse(
        f"{'.'.join(str(x) for x in parsed_version.parts)}.post{new_post_release_num}"
    )
    print(f"New version of `{package_name}` will be: {updated_version}")

    return updated_version.to_string()


def main() -> None:
    """Run the script to create the new version number."""
    # Load in the GitHub Action inputs
    # See https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#example-specifying-inputs
    package_name = os.environ["INPUT_PACKAGE-NAME"]
    # Connect to the test.pypi.org server
    test_pypi_server = PyPISimple("https://test.pypi.org/simple/")
    print(f"Checking for the latest version of `{package_name}` on test.pypi.org...")

    # Load in the current data from the pyproject.toml file to
    # read the current, local package version
    with PYPROJECT_FILE.open("rb") as file_handle:
        pyproject_data = tomli.load(file_handle)
        local_version = pyproject_data["tool"]["poetry"]["version"]
    # Get the latest version of the package on test.pypi.org and create the new version
    updated_version = create_new_post_version(
        package_name,
        test_pypi_server.get_project_page(package_name).packages[-1].version,
        local_version,
    )

    # Update the pyproject.toml file with the new version number
    print("Updating the pyproject.toml file with the new version...")
    # Modify the version value
    pyproject_data["tool"]["poetry"]["version"] = updated_version
    # Write back the data to the file
    with PYPROJECT_FILE.open("wb") as file_handle:
        tomli_w.dump(pyproject_data, file_handle)

    # Set the output variable for GitHub Actions
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as github_output_file_handle:  # noqa: PTH123
        github_output_file_handle.write(f"new-version={updated_version}\n")


if __name__ == "__main__":  # pragma: no cover
    # Run the main function
    main()
