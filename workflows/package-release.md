# package-release.yml

This workflow will create a new release of the package using the
[`python-semantic-release`](https://python-semantic-release.readthedocs.io/en/latest/) tool.
It will then build the package, upload the package to
[TestPyPI](https://test.pypi.org) and [PyPI](https://pypi.org),
create a new GitHub Release for the project,
and then verify that the package can be installed from
[TestPyPI](https://test.pypi.org) and [PyPI](https://pypi.org).

This workflow runs an action that will populate two files in the
[`python-semantic-release` templates directory](https://python-semantic-release.readthedocs.io/en/stable/configuration/configuration.html#template-dir).
One of those files will contain the contents of the `CHANGELOG.md` file in the
repo prior to creating the new release. The other file will contain the
contents of the `## Unreleased` section of the `CHANGELOG.md` file that
will be used to fill in the GitHub Release Notes.

> [!IMPORTANT]
> This workflow requires the `CHANGELOG.md` file to be in a format that is based on
> [Keep a Changelog](https://keepachangelog.com)
> (the primary difference is the `## [Unreleased]` section is replaced by an `## Unreleased` section),
> and this project adheres to [Semantic Versioning](https://semver.org). See this repo's
> [CHANGELOG.md](../CHANGELOG.md) for an example of the format to use.
>
> Valid subsections within a version are:
>
> - Added
> - Changed
> - Deprecated
> - Removed
> - Fixed
> - Security

> [!IMPORTANT]
> This workflow uses several GitHub Actions environments.
>
> The `bump-version` job runs in the
> `package-release-gate` environment. It is recommended to limit this environment to only the
> `main` branch as well as enable the `Required reviewers` setting to enforce approval
> before creating a new release of the package. It is also recommended to store the token used
> to check out the repo and the SSH public/private keys as environment secrets so that
> they can only be used by the `package-release-gate` environment. These secrets will need to be
> passed in as secrets when calling the reusable workflow, see the [example](#example) below.
>
> The `upload-testpypi` job (run when `inputs.build-and-publish-python-package == true`) runs in the `package-testpypi` environment. It is recommended to
> limit this environment to only the `main` branch. It is also recommended to store the token
> for uploading to [test.pypi.org](https://test.pypi.org) as an environment secret so that it can only be
> accessed by the `package-testpypi` environment. This secret will need to be passed in as a
> secret when calling the reusable workflow, see the [example](#example) below.
>
> The `upload-pypi` job (run when `inputs.build-and-publish-python-package == true`) runs in the `package-release` environment. It is recommended to
> limit this environment to only the `main` branch. It is also recommended to store the token
> for uploading to [pypi.org](https://pypi.org) as an environment secret so that it can only be
> accessed by the `package-release` environment. This secret will need to be passed in as a
> secret when calling the reusable workflow, see the [example](#example) below.

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

> [!NOTE]
> This workflow uses the following GitHub Actions:
>
> - [actions/checkout](https://github.com/actions/checkout)
> - [tektronix/python-package-ci-cd/actions/find_unreleased_changelog_items](https://github.com/tektronix/python-package-ci-cd)
> - [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
> - [hynek/build-and-inspect-python-package](https://github.com/hynek/build-and-inspect-python-package)
> - [actions/download-artifact](https://github.com/actions/download-artifact)
> - [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
> - [python-semantic-release/upload-to-gh-release](https://github.com/python-semantic-release/upload-to-gh-release)
> - [actions/setup-python](https://github.com/actions/setup-python)
> - [nick-fields/retry](https://github.com/nick-fields/retry)
>
> See the [Workflow file][workflow-file] for the currently used versions of each GitHub Action.

> [!TIP]
> See the [Workflow file][workflow-file] for implementation details.

## Inputs

| Input variable                     | Necessity | Description                                                                                                                                                                                    | Default                                     |
| ---------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `package-name`                     | required  | The name of the package to build, upload, and install.                                                                                                                                         |                                             |
| `repo-name`                        | required  | The full name of the repository to use to gate uploads, in the format `owner/repo`.                                                                                                            |                                             |
| `commit-user-name`                 | required  | The name of the user to use when committing changes to the repository.                                                                                                                         |                                             |
| `commit-user-email`                | required  | The email of the user to use when committing changes to the repository.                                                                                                                        |                                             |
| `release-level`                    | required  | The level of the release to create. Must be one of `major`, `minor`, or `patch`.                                                                                                               |                                             |
| `build-and-publish-python-package` | optional  | A boolean value that determines whether to build and publish the Python package. If set to `false`, the package binaries will not be built or published to PyPI, TestPyPI, or GitHub Releases. | `true`                                      |
| `python-versions-array`            | optional  | A valid JSON array of Python versions to test against. If `inputs.build-and-publish-python-package` is set to `true`, this input must be provided or the build will fail.                      |                                             |
| `operating-systems-array`          | optional  | A valid JSON array of operating system names to run tests on.                                                                                                                                  | `'["ubuntu", "windows", "macos"]'`          |
| `previous-changelog-filepath`      | optional  | The full path of the file to copy the contents of the changelog into for use in the `python-semantic-release` templates.                                                                       | `'.previous_changelog_for_template.md'`     |
| `previous-release-notes-filepath`  | optional  | The full path of the file to copy the contents of the `## Unreleased` section of the changelog into for use in the GitHub Release Notes.                                                       | `'.previous_release_notes_for_template.md'` |

## Secrets

| Secret variable           | Necessity | Description                                                                                                                                                        |
| ------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `checkout-token`          | required  | The token to use for checking out the repository, must have permissions to write back to the repository.                                                           |
| `ssh-signing-key-private` | required  | A private SSH key associated with the account that owns the `checkout-token` that will be used to sign the commit and tag created by `python-semantic-release`.    |
| `ssh-signing-key-public`  | required  | The public SSH key linked to the `secrets.ssh-signing-key-private` key that will be used to sign the commit and tag created by `python-semantic-release`.          |
| `pypi-api-token`          | required  | The API token for the package on pypi.org. If `inputs.build-and-publish-python-package` is set to `true`, this input must be provided or the build will fail.      |
| `test-pypi-api-token`     | required  | The API token for the package on test.pypi.org. If `inputs.build-and-publish-python-package` is set to `true`, this input must be provided or the build will fail. |

> [!CAUTION]
> If a Python package is intended to be built and published, **the `pypi-api-token` and `test-pypi-api-token` secrets must be provided**.

## Example

```yaml
name: Package Release
on:
  workflow_dispatch:
    inputs:
      release-level:
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
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-package-release.yml@v1.8.2
    with:
      package-name: my-package  # required
      repo-name: owner/my-package  # required
      commit-user-name: 'User Name'
      commit-user-email: 'user-email'
      release-level: ${{ inputs.release-level }}  # required
      build-and-publish-python-package: true  # optional
      python-versions-array: '["3.9", "3.10", "3.11", "3.12"]'  # optional
      operating-systems-array: '["ubuntu", "windows", "macos"]'  # optional
      previous-changelog-filepath: 'templates/.previous_changelog_for_template.md'  # optional
      previous-release-notes-filepath: 'templates/.previous_release_notes_for_template.md'  # optional
    permissions:
      contents: write
      id-token: write
      attestations: write
    secrets:
      checkout-token: ${{ secrets.CHECKOUT_TOKEN }}  # required for the `bump-version` job, recommended to store this in the `package-release-gate` environment
      ssh-signing-key-private: ${{ secrets.SSH_SIGNING_KEY_PRIVATE }}  # required for the `bump-version` job, recommended to store this in the `package-release-gate` environment
      ssh-signing-key-public: ${{ secrets.SSH_SIGNING_KEY_PUBLIC }}  # required for the `bump-version` job, recommended to store this in the `package-release-gate` environment
      pypi-api-token: ${{ secrets.PYPI_API_TOKEN }}  # required for the `upload-pypi` job (run when `inputs.build-and-publish-python-package == true`), recommended to store this in the `package-release` environment
      test-pypi-api-token: ${{ secrets.TEST_PYPI_API_TOKEN }}  # required for the `upload-testpypi` job (run when `inputs.build-and-publish-python-package == true`), recommended to store this in the `package-testpypi` environment
```

[workflow-file]: ../.github/workflows/_reusable-package-release.yml
