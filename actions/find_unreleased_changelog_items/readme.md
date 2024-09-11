# find_unreleased_changelog_items

This action will parse the repository's `CHANGELOG.md` file to determine if
there are any unreleased items. It will fail if it cannot find any unreleased
items, as this means that the package is not ready for a new release. This action will also
fail if it cannot find any merged PRs since the last release, as this also means that the
package is not ready for a new release.

This action will populate two files in the
[`python-semantic-release` templates directory](https://python-semantic-release.readthedocs.io/en/latest/configuration.html#config-changelog-template-dir).
One of those files will contain the contents of the `CHANGELOG.md` file in the
repo prior to creating the new release. The other file will contain the
contents of the `## Unreleased` section of the `CHANGELOG.md` file that
will be used to fill in the GitHub Release Notes.

> [!IMPORTANT]
> This action requires that the `pyproject.toml` and `CHANGELOG.md` files exist in the
> current working directory and that all tags are fetched from the remote repository.

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

| Input variable                    | Necessity | Description                                                                                                                                                                                                                         | Default                                     |
| --------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `release-level`                   | optional  | The level of the impending release. Must be one of `major`, `minor`, or `patch`. Setting this input will trigger the action to output the summary of the incoming release level and the unreleased changes to the Workflow Summary. |                                             |
| `previous-changelog-filepath`     | optional  | The full path of the file to copy the contents of the changelog into for use in the `python-semantic-release` templates.                                                                                                            | `'.previous_changelog_for_template.md'`     |
| `previous-release-notes-filepath` | optional  | The full path of the file to copy the contents of the `## Unreleased` section of the changelog into for use in the GitHub Release Notes.                                                                                            | `'.previous_release_notes_for_template.md'` |

## Example

```yaml
jobs:
  # Print the inputs to the summary page for easy User Review
  print-inputs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@692973e3d937129bcbf40652eb9f2f61becf3332
        with:
          fetch-depth: 0
          fetch-tags: true
      - uses: tektronix/python-package-ci-cd/actions/find_unreleased_changelog_items@v1.4.0
        with:
          release-level: ${{ inputs.release-level }}  # optional
          previous-changelog-filepath: .previous_changelog_for_template.md  # optional
          previous-release-notes-filepath: .previous_release_notes_for_template.md  # optional
```
