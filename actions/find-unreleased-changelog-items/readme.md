# find-unreleased-changelog-items

This action will parse the repository's `CHANGELOG.md` file to determine if
there are any unreleased items. It will fail if it cannot find any unreleased
items, as this means that the package is not ready for a new release.

This action will populate two files in the
[`python-semantic-release` templates directory](https://python-semantic-release.readthedocs.io/en/latest/configuration.html#config-changelog-template-dir).
One of those files will contain the contents of the `CHANGELOG.md` file in the
repo prior to creating the new release. The other file will contain the
contents of the `## Unreleased` section of the `CHANGELOG.md` file that
will be used to fill in the GitHub Release Notes.

> [!IMPORTANT]
> This action requires the `CHANGELOG.md` file to be in a format that is based on
> [Keep a Changelog](https://keepachangelog.com)
> (the primary difference is the `## [Unreleased]` section is replaced by an `## Unreleased` section),
> and this project adheres to [Semantic Versioning](https://semver.org). See this repo's
> [CHANGELOG.md](../../CHANGELOG.md) for an example of the format to use.
>
> Valid subsections within a version are:
>
> - Added
> - Changed
> - Deprecated
> - Removed
> - Fixed
> - Security

## Inputs

| Input variable                    | Necessity | Description                                                                                                                                                                                                                                                                             | Default                                     |
| --------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `release-level`                   | required  | The level of the impending release. Must be one of `major`, `minor`, or `patch`. Setting this input will trigger the action to output the summary of the incoming release level and the unreleased changes to the Workflow Summary.                                                     |                                             |
| `previous-changelog-filename`     | optional  | The name of the file to copy the contents of the changelog into for use in the `python-semantic-release` templates. This file will be created inside of the directory defined by the `[tool.semantic_release.changelog.template_dir]` key in the `pyproject.toml` file.                 | `'.previous_changelog_for_template.md'`     |
| `previous-release-notes-filename` | optional  | The name of the file to copy the contents of the `## Unreleased` section of the changelog into for use in the GitHub Release Notes. This file will be created inside of the directory defined by the `[tool.semantic_release.changelog.template_dir]` key in the `pyproject.toml` file. | `'.previous_release_notes_for_template.md'` |

## Example

```yaml
jobs:
  # Print the inputs to the summary page for easy User Review
  print-inputs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: tektronix/python-package-ci-cd/actions/find-unreleased-changelog-items@main  # it is recommended to use the latest release tag instead of `main`
        with:
          release-level: ${{ inputs.release-level }}  # optional
          previous-changelog-filename: .previous_changelog_for_template.md  # optional
          previous-release-notes-filename: .previous_release_notes_for_template.md  # optional
```
