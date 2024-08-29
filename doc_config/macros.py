"""Macros for the documentation."""

import os
import pathlib
import re

import tomli

from mkdocs_macros.plugin import MacrosPlugin  # pyright: ignore[reportMissingTypeStubs]

NEWLINE_AND_TAB = "\n    "
CONVERSION_PATTERN = re.compile(
    r"> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION|DANGER)]\s*>\s*(.*?)(?=\n[^>]|$)",
    re.IGNORECASE | re.DOTALL,
)


####################################################################################################
# Helper functions
####################################################################################################
def convert_gfm_alerts_to_admonitions(content: str) -> str:
    """Convert GitHub Flavored Markdown (GFM) alerts to MkDocs admonitions.

    Args:
        content: The content to convert.

    Returns:
        The updated content with GFM alerts converted to markdown admonitions.
    """

    def replace_match(match: re.Match[str]) -> str:
        """Replace the matched GFM alert with an admonition.

        Args:
            match: The matched GFM alert.

        Returns:
            The replacement text.
        """
        alert_type = match.group(1).lower()
        text = match.group(2).strip()
        # Replace initial '>' from subsequent lines
        text = text.replace("\n>", "\n")
        # Replace with admonition format
        return f"!!! {alert_type}\n    " + text.replace("\n", "\n    ")

    return re.sub(CONVERSION_PATTERN, replace_match, content)


def convert_local_repo_links_to_urls(content: str, base_repo_url: str) -> str:
    """Convert local repository links to URLs.

    Args:
        content: The content to convert.
        base_repo_url: The base URL of the repository.

    Returns:
        The updated content with local repository links converted to URLs.
    """
    return content.replace("]: ../.github", f"]: {base_repo_url}/.github")


####################################################################################################
# Macro functions
####################################################################################################


####################################################################################################
# Mkdocs Macros functions
####################################################################################################
def define_env(env: MacrosPlugin) -> None:
    """Define variables, macros and filters.

    Notes:
        - variables: the dictionary that contains the environment variables
        - macro: a decorator function, to declare a macro.
        - filter: a function with one of more arguments,
            used to perform a transformation
    """
    # Read in the current package version number to use in templates and files
    with open(  # noqa: PTH123
        pathlib.Path(f"{pathlib.Path(__file__).parents[1]}") / "pyproject.toml", "rb"
    ) as file_handle:
        pyproject_data = tomli.load(file_handle)
        package_version = "v" + pyproject_data["tool"]["poetry"]["version"]
    git_ref = "main" if os.getenv("READTHEDOCS_VERSION") == "latest" else package_version

    # Add a variable that points to the latest version of the package
    env.variables["package_version"] = package_version
    # Add a variable that points to either the latest version tag or the main branch depending
    # on where/when the docs are being built.
    env.variables["git_ref"] = git_ref


def on_pre_page_macros(env: MacrosPlugin) -> None:
    """Post-process pages."""
    # Check if there are any repo links to replace on the page
    env.markdown = convert_local_repo_links_to_urls(
        env.markdown,  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
        f"{env.conf.repo_url}/blob/{env.variables['git_ref']}/",
    )


def on_post_page_macros(env: MacrosPlugin) -> None:
    """Post-process pages."""
    # Check if there are any admonitions to replace on the page
    env.markdown = convert_gfm_alerts_to_admonitions(env.markdown)  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
