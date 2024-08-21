"""Create a unique post-release version for test.pypi.org.

This script will find the latest version of the package on test.pypi.org and create a new
post-release version, incrementing the `.postN` version if necessary. It will then write that
new version number back to the pyproject.toml file.

This script will also set the value of a GitHub Actions output variable named `new-version` to the
newly created version number.

This script needs to be run from a directory that contains a `pyproject.toml` file.
"""

import os
import pathlib

import tomli
import tomli_w

from poetry.core.constraints.version import Version
from pypi_simple import PyPISimple

_ENV_VAR_TRUE_VALUES = {"1", "true", "yes"}

PYPROJECT_FILE = pathlib.Path("./pyproject.toml")


def main() -> None:
    """Run the script to create the new version number."""
    # Load in the GitHub Action inputs
    # See https://docs.github.com/en/actions/sharing-automations/creating-actions/metadata-syntax-for-github-actions#example-specifying-inputs
    package_name = os.environ["INPUT_PACKAGE-NAME"]
    # Connect to the test.pypi.org server
    test_pypi_server = PyPISimple("https://test.pypi.org/simple/")
    print(f"Checking for the latest version of `{package_name}` on test.pypi.org...")

    # Get the latest version of the package on test.pypi.org
    latest_version = Version.parse(
        test_pypi_server.get_project_page(package_name).packages[-1].version  # pyright: ignore[reportArgumentType]
    )
    print(f"Current version of `{package_name}` is: {latest_version}")

    # Create the .postN version suffix
    new_post_release_num = 1
    if latest_version.post:
        new_post_release_num += latest_version.post.number

    # Create the new version number
    updated_version = Version.parse(
        f"{'.'.join(str(x) for x in latest_version.parts)}.post{new_post_release_num}"
    )
    print(f"New version of `{package_name}` will be: {updated_version}")

    # Update the pyproject.toml file with the new version number (only if running in GitHub Actions)
    print("Updating the pyproject.toml file with the new version...")
    # Read in the current data
    with PYPROJECT_FILE.open("rb") as file_handle:
        pyproject_data = tomli.load(file_handle)
    # Modify the version value
    pyproject_data["tool"]["poetry"]["version"] = updated_version.to_string()
    # Write back the data to the file
    with PYPROJECT_FILE.open("wb") as file_handle:
        tomli_w.dump(pyproject_data, file_handle)

    # Set the output variable for GitHub Actions
    with open(os.environ["GITHUB_OUTPUT"], "a") as github_output_file_handle:  # noqa: PTH123
        github_output_file_handle.write(f"new-version={updated_version}\n")


if __name__ == "__main__":
    # Run the main function
    main()
