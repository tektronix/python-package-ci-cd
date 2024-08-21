# update-python-and-pre-commit-dependencies.yml

This workflow updates Python development dependencies using the
[Poetry](https://python-poetry.org/) package manager in-sync with
[`pre-commit`](https://pre-commit.com/) hooks when triggered as a part of
[Dependabot](https://docs.github.com/en/code-security/getting-started/dependabot-quickstart-guide)
updates for the Python dependencies.

> [!IMPORTANT]
> When calling this reusable workflow, the permissions must be set as follows:
>
> ```yaml
> permissions:
>   contents: write
> ```

> [!NOTE]
> This workflow uses the following GitHub Actions:
>
> - [actions/checkout](https://github.com/actions/checkout)
> - [crazy-max/ghaction-import-gpg](https://github.com/crazy-max/ghaction-import-gpg)
> - [tektronix/python-package-ci-cd/actions/update-development-dependencies](https://github.com/tektronix/python-package-ci-cd)
> - [stefanzweifel/git-auto-commit-action](https://github.com/stefanzweifel/git-auto-commit-action)
>
> See the [Workflow file][workflow-file] for the currently used versions of each GitHub Action.

> [!TIP]
> See the [Workflow file][workflow-file] for implementation details.

## Inputs

| Input variable              | Necessity | Description                                                                                                                                                                                                                         | Default |
| --------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `commit-user-name`          | required  | The name of the user to use when committing changes to the repository.                                                                                                                                                              |         |
| `commit-user-email`         | required  | The email of the user to use when committing changes to the repository.                                                                                                                                                             |         |
| `dependency-dict`           | optional  | Specify a valid dictionary of dependency groups to update, where each key is a dependency group name, and each value is a tuple of dependencies to update within that group, e.g. `{"dev": ("pylint", "ruff"), "tests": ("ruff")}`. | `{}`    |
| `update-pre-commit`         | optional  | A boolean indicating if the pre-commit hooks should be updated.                                                                                                                                                                     | `false` |
| `run-pre-commit`            | optional  | A boolean indicating to run the pre-commit hooks to perform auto-fixing after updating the dependencies. Setting this input to `true` will also set the update-pre-commit input to `true`.                                          | `false` |
| `pre-commit-hook-skip-list` | optional  | A comma-separated list of pre-commit hooks to skip (only applicable when `run-pre-commit=true`).                                                                                                                                    | `""`    |
| `export-dependency-groups`  | optional  | A comma-separated list of dependency groups to export to a `requirements.txt` file. The format is `group1,group2:custom-path/to/test/folder`.                                                                                       | `""`    |

## Secrets

| Secret variable              | Necessity | Description                                                                                              |
| ---------------------------- | --------- | -------------------------------------------------------------------------------------------------------- |
| `checkout-token`             | required  | The token to use for checking out the repository, must have permissions to write back to the repository. |
| `gpg-signing-key-private`    | required  | The private GPG key to use for signing the commit.                                                       |
| `gpg-signing-key-passphrase` | required  | The passphrase for the private GPG key.                                                                  |

## Example

```yaml
name: Update python linting dependencies in-sync with pre-commit
on:
  pull_request:
    branches: [main]
jobs:
  update-python-and-pre-commit-dependencies:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-update-python-and-pre-commit-dependencies.yml@main  # it is recommended to use the latest release tag instead of `main`
    with:
      commit-user-name: 'User Name'
      commit-user-email: 'user-email'
      dependency-dict: '{"dev": ("pylint", "ruff"), "tests": ("ruff")}'  # optional, but without it nothing will get updated by Poetry
      update-pre-commit: true  # optional
      run-pre-commit: true  # optional
      pre-commit-hook-skip-list: pylint,pyright,pyroma,poetry-audit  # optional, hooks that don't auto-fix things can (and probably should be) skipped
      export-dependency-groups: 'docs,tests:custom-path/to/test/folder'  # optional
    permissions:
      contents: write
    secrets:
      checkout-token: ${{ secrets.CHECKOUT_TOKEN }}
      gpg-signing-key-private: ${{ secrets.GPG_SIGNING_KEY_PRIVATE }}
      gpg-signing-key-passphrase: ${{ secrets.GPG_SIGNING_KEY_PASSPHRASE }}
```

[workflow-file]: ../.github/workflows/_reusable-update-python-and-pre-commit-dependencies.yml
