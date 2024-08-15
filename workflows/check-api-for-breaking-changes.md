# check-api-for-breaking-changes.yml

This workflow will use the [`griffe`](https://mkdocstrings.github.io/griffe/) package to check for
any major or breaking changes in a package's API. It requires that the package be using the
`src` package layout. It runs on the `ubuntu-latest` runner label.
It uploads a file called `breaking_changes.md` as a workflow artifact that can be used with the
`publish-api-comparison.yml` workflow to post a comment on Pull Requests with details of changed APIs.

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
      tektronix/python-package-ci-cd/workflows/check-api-for-breaking-changes.yml@v0.1.0
    with:
      package-name: my_package_name  # required
```
