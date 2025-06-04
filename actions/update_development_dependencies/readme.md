# update_development_dependencies

This action enables updating Python development dependencies using the
[Poetry](https://python-poetry.org/) package manager in-sync with
[`pre-commit`](https://pre-commit.com/) hooks.

> [!IMPORTANT]
> If the job that is using this action needs to commit the changes that this action makes, the job
> must have at least the following permissions:
>
> ```yaml
> permissions:
>   contents: write
> ```
>
> The code must also be checked out by a user with write permissions to the repository. This
> means that the default `GITHUB_TOKEN` for the
> [`actions/checkout`](https://github.com/actions/checkout) step will more than
> likely not allow the changes made by this action to be committed back to the repository.

## Inputs

| Input variable                     | Necessity | Description                                                                                                                                                                                                                                                                                                              | Default |
| ---------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------- |
| `repo-root`                        | optional  | The root directory of the repository.                                                                                                                                                                                                                                                                                    | `.`     |
| `install-dependencies`             | optional  | A boolean indicating if packages should be installed via poetry (this is not usually needed).                                                                                                                                                                                                                            | `false` |
| `dependency-dict`                  | optional  | Specify a valid JSON dictionary of dependency groups to update, where each key is a dependency group name, and each value is a list of dependencies to update within that group, e.g. `'{"dev": ["pylint", "ruff"], "tests": ["ruff"]}'`. Use an empty string, e.g. `""`, for dependencies located in the default group' | `{}`    |
| `update-pre-commit`                | optional  | A boolean indicating if the pre-commit hooks should be updated.                                                                                                                                                                                                                                                          | `false` |
| `run-pre-commit`                   | optional  | A boolean indicating to run the pre-commit hooks to perform auto-fixing after updating the dependencies. Setting this input to `true` will also set the update-pre-commit input to `true`.                                                                                                                               | `false` |
| `pre-commit-repo-update-skip-list` | optional  | A comma-separated list of pre-commit repo urls to skip updates for (only applicable when `update-pre-commit=true`).                                                                                                                                                                                                      | `""`    |
| `pre-commit-hook-skip-list`        | optional  | A comma-separated list of pre-commit hooks to skip (only applicable when `run-pre-commit=true`).                                                                                                                                                                                                                         | `""`    |
| `export-dependency-groups`         | optional  | A comma-separated list of dependency groups to export to a `requirements.txt` file. The format is `group1,group2:custom-path/to/test/folder`.                                                                                                                                                                            | `""`    |

## Example

```yaml
jobs:
  update-python-and-pre-commit-deps:
    name: Update python linters and pre-commit dependencies
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@692973e3d937129bcbf40652eb9f2f61becf3332
        with:
          fetch-depth: 0
          ref: ${{ github.head_ref }}
          token: ${{ secrets.checkout-token }}

      - uses: tektronix/python-package-ci-cd/actions/update_development_dependencies@v1.7.5
        with:
          repo-root: .  # optional, defaults to the current working directory
          install-dependencies: false  # optional, this will almost never need to be set to true
          dependency-dict: '{"dev": ["pylint", "ruff"], "tests": ["ruff"]}'  # optional, but without it nothing will get updated by Poetry
          update-pre-commit: true  # optional
          run-pre-commit: true  # optional
          pre-commit-repo-update-skip-list: 'https://github.com/pre-commit/pre-commit-hooks'  # optional
          pre-commit-hook-skip-list: 'pylint'  # optional, hooks that don't auto-fix things can (and probably should be) skipped
          export-dependency-groups: 'docs,tests:custom-path/to/test/folder'  # optional

      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: 'chore: Update python dependencies and pre-commit dependencies.'
          commit_user_name: 'User Name'
          commit_user_email: 'user-email'
          commit_author: User Name <user-email>
```
