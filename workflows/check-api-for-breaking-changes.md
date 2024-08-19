# check-api-for-breaking-changes.yml

This workflow will use the [`griffe`](https://mkdocstrings.github.io/griffe/) package to check for
any major or breaking changes in a package's API. It requires that the package be using the
`src` package layout and the [Poetry package manager](https://python-poetry.org/). It runs on the
`ubuntu-latest` runner label, uses the
default version of Python available on the runner, will install the package from the current
working directory of the calling repository using `pip install --upgrade .`, and will use the latest
compatible version of [`griffe`](https://pypi.org/project/griffe/) to check for changes.
It uploads a file called `breaking_changes.md` as a workflow artifact that can be used with the
`publish-api-comparison.yml` workflow to post a comment on Pull Requests with details of changed APIs.

> [!TIP]
> See the [Workflow file](../.github/workflows/_reusable-check-api-for-breaking-changes.yml) for implementation details.

## Inputs

| Input variable | Necessity | Description                                            | Default |
| -------------- | --------- | ------------------------------------------------------ | ------- |
| `package-name` | required  | The name of the package to check for breaking changes. |         |

## Example

```yaml
# .github/workflows/check-api-for-breaking-changes.yml
name: Check Public API for Breaking Changes
on:
  pull_request:
    branches: [main]
jobs:
  check-api-for-breaking-changes:
    uses:
      tektronix/python-package-ci-cd/.github/workflows/_reusable-check-api-for-breaking-changes.yml@main  # it is recommended to use the latest release tag instead of `main`
    with:
      package-name: my_package_name  # required
```
