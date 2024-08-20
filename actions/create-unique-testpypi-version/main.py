"""Create a unique post-release version for test.pypi.org.

This script will find the latest version of the package on test.pypi.org and create a new
post-release version, incrementing the `.postN` version if necessary. It will then write that
new version number back to the pyproject.toml file.

This script will also set the value of a GitHub Actions output variable named `new-version` to the
newly created version number.
"""

import argparse
import os
import pathlib
import sys

import tomli
import tomli_w

from poetry.core.constraints.version import Version
from pypi_simple import PyPISimple

_ENV_VAR_TRUE_VALUES = {"1", "true", "yes"}
RUNNING_IN_GITHUB_ACTIONS = bool(os.getenv("GITHUB_ACTION"))

PYPROJECT_FILE = pathlib.Path("./pyproject.toml")


def _parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments.

    Returns:
        The parsed Namespace.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--package",
        required=True,
        action="store",
        dest="package",
        help="Provide the name of the package on test.pypi.org",
    )

    return parser.parse_args()


def main() -> str:
    """Run the script to create the new version number.

    Returns:
        The new version number.
    """
    args = _parse_arguments()
    package: str = args.package
    test_pypi_server = PyPISimple("https://test.pypi.org/simple/")
    print(f"Checking for the latest version of `{package}` on test.pypi.org...")

    # Get the latest version of the package on test.pypi.org
    latest_version = Version.parse(test_pypi_server.get_project_page(package).packages[-1].version)  # pyright: ignore[reportArgumentType]
    print(f"Current version of `{package}` is: {latest_version}")

    # Create the .postN version suffix
    new_post_release_num = 1
    if latest_version.post:
        new_post_release_num += latest_version.post.number

    # Create the new version number
    updated_version = Version.parse(
        f"{'.'.join(str(x) for x in latest_version.parts)}.post{new_post_release_num}"
    )
    print(f"New version of `{package}` will be: {updated_version}")

    # Update the pyproject.toml file with the new version number (only if running in GitHub Actions)
    if RUNNING_IN_GITHUB_ACTIONS:
        print("Updating the pyproject.toml file with the new version...")
        # Read in the current data
        with PYPROJECT_FILE.open("rb") as file_handle:
            pyproject_data = tomli.load(file_handle)
        # Modify the version value
        pyproject_data["tool"]["poetry"]["version"] = updated_version.to_string()
        # Write back the data to the file
        with PYPROJECT_FILE.open("wb") as file_handle:
            tomli_w.dump(pyproject_data, file_handle)

    return updated_version.to_string()


if __name__ == "__main__":
    # Handle GitHub Actions environment variables
    # See https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables
    if RUNNING_IN_GITHUB_ACTIONS:
        sys.argv.extend(["--package", os.getenv("INPUT_PACKAGE-NAME", "")])

    # Run the main function
    new_version = main()

    # Set the output variable for GitHub Actions
    if RUNNING_IN_GITHUB_ACTIONS:
        with open(os.environ["GITHUB_OUTPUT"], "a") as github_output_file_handle:  # noqa: PTH123
            github_output_file_handle.write(f"new-version={new_version}\n")
