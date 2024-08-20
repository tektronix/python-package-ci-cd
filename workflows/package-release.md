# package-release.yml

This workflow will create a new release of the package using the
[`python-semantic-release`](https://python-semantic-release.readthedocs.io/en/latest/) tool.
It will then build the package, upload the package to
[TestPyPI](https://test.pypi.org) and [PyPI](https://pypi.org),
and then verify that the package can be installed from
[TestPyPI](https://test.pypi.org) and [PyPI](https://pypi.org).

This workflow runs an action that will populate two files in the
[`python-semantic-release` templates directory](https://python-semantic-release.readthedocs.io/en/latest/configuration.html#config-changelog-template-dir).
One of those files will contain the contents of the `CHANGELOG.md` file in the
repo prior to creating the new release. The other file will contain the
contents of the `## Unreleased` section of the `CHANGELOG.md` file that
will be used to fill in the GitHub Release Notes.

> [!IMPORTANT]
> When calling this reusable workflow, the permissions must be set as follows:
>
> ```yaml
> permissions:
>   contents: write
>   id-token: write
>   attestations: write
> ```

> [!NOTE]
> This workflow uses concurrency to limit the number of builds that can run at the same time
> to a single build. This concurrency is shared across the `'pypi (Reusable Workflows)'` concurrency
> group within the repo that calls this workflow.

> [!TIP]
> See the [Workflow file](../.github/workflows/_reusable-package-release.yml) for implementation details.

## Inputs

| Input variable                    | Necessity | Description                                                                                                                                                                                                                                                                             | Default                                     |
| --------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `package-name`                    | required  | The name of the package to build, upload, and install.                                                                                                                                                                                                                                  |                                             |
| `repo-name`                       | required  | The full name of the repository to use to gate uploads, in the format `owner/repo`.                                                                                                                                                                                                     |                                             |
| `commit-user-name`                | required  | The name of the user to use when committing changes to the repository.                                                                                                                                                                                                                  |                                             |
| `commit-user-email`               | required  | The email of the user to use when committing changes to the repository.                                                                                                                                                                                                                 |                                             |
| `release-level`                   | required  | The level of the release to create. Must be one of `major`, `minor`, or `patch`.                                                                                                                                                                                                        |                                             |
| `python-versions-array`           | required  | A valid JSON array of Python versions to test against.                                                                                                                                                                                                                                  |                                             |
| `operating-systems-array`         | optional  | A valid JSON array of operating system names to run tests on.                                                                                                                                                                                                                           | `'["ubuntu", "windows", "macos"]'`          |
| `previous-changelog-filename`     | optional  | The name of the file to copy the contents of the changelog into for use in the `python-semantic-release` templates. This file will be created inside of the directory defined by the `[tool.semantic_release.changelog.template_dir]` key in the `pyproject.toml` file.                 | `'.previous_changelog_for_template.md'`     |
| `previous-release-notes-filename` | optional  | The name of the file to copy the contents of the `## Unreleased` section of the changelog into for use in the GitHub Release Notes. This file will be created inside of the directory defined by the `[tool.semantic_release.changelog.template_dir]` key in the `pyproject.toml` file. | `'.previous_release_notes_for_template.md'` |

## Secrets

| Secret variable           | Necessity | Description                                                                                                                                                     |
| ------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `checkout-token`          | required  | The token to use for checking out the repository, must have permissions to write back to the repository.                                                        |
| `ssh-signing-key-private` | required  | A private SSH key associated with the account that owns the `checkout-token` that will be used to sign the commit and tag created by `python-semantic-release`. |
| `ssh-signing-key-public`  | required  | The public SSH key linked to the `secrets.ssh-signing-key-private` key that will be used to sign the commit and tag created by `python-semantic-release`.       |

## Example

```yaml
name: Package Release
on:
  workflow_dispatch:
    inputs:
      release_level:
        type: choice
        required: true
        description: |
          Select the release level:
          patch for backward compatible minor changes and bug fixes,
          minor for backward compatible larger changes,
          major for non-backward compatible changes.
        options: [patch, minor, major]
concurrency:  # This concurrency is not required, but can be added if extra control of concurrent builds is required
  group: pypi
jobs:
  package-release:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-package-release.yml@main  # it is recommended to use the latest release tag instead of `main`
    with:
      package-name: my-package  # required
      repo-name: owner/my-package  # required
      commit-user-name: 'User Name'
      commit-user-email: 'user-email'
      release_level: ${{ inputs.release_level }}  # required
      python-versions-array: '["3.9", "3.10", "3.11", "3.12"]'  # required
      operating-systems-array: '["ubuntu", "windows", "macos"]'  # optional
      previous-changelog-filename: '.previous_changelog_for_template.md'  # optional
      previous-release-notes-filename: '.previous_release_notes_for_template.md'  # optional
    permissions:
      contents: write
      id-token: write
      attestations: write
    secrets:
      checkout-token: ${{ secrets.CHECKOUT_TOKEN }}
      ssh-signing-key-private: ${{ secrets.SSH_SIGNING_KEY_PRIVATE }}
      ssh-signing-key-public: ${{ secrets.SSH_SIGNING_KEY_PUBLIC }}
```
