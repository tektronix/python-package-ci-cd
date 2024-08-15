<div markdown="1" class="custom-badge-table">

|                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Code Quality** | [![CodeQL status](https://github.com/tektronix/python-package-ci-cd/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/tektronix/python-package-ci-cd/actions/workflows/codeql-analysis.yml) [![CodeFactor grade](https://www.codefactor.io/repository/github/tektronix/python-package-ci-cd/badge)](https://www.codefactor.io/repository/github/tektronix/python-package-ci-cd) [![pre-commit status](https://results.pre-commit.ci/badge/github/tektronix/python-package-ci-cd/main.svg)](https://results.pre-commit.ci/latest/github/tektronix/python-package-ci-cd/main) |

</div>

---

# python-package-ci-cd: GitHub Actions and Re-usable Workflows for Python Packaging CI/CD

`python-package-ci-cd` is a collection of GitHub Actions and re-usable Workflows that enable
Python Packaging CI/CD.

## Actions

### Usage

## Reusable Workflows

### check-api-for-breaking-changes

This workflow will use the [`griffe`](https://mkdocstrings.github.io/griffe/) package to check for
any major or breaking changes in a package's API. It requires that the package be using the
`src` package layout. It runs on the `ubuntu-latest` runner label.
It uploads a file called `breaking_changes.md` as a workflow artifact that can be used with the
`publish-api-comparison.yml` workflow to post a comment on Pull Requests with details of changed APIs.

Usage Example:

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

## Maintainers

Before reaching out to any maintainers directly, please first check if
your issue or question is already covered by any [open
issues](https://github.com/tektronix/python-package-ci-cd/issues). If the issue or
question you have is not already covered, please [file a new
issue](https://github.com/tektronix/python-package-ci-cd/issues/new/choose) or
start a
[discussion](https://github.com/tektronix/python-package-ci-cd/discussions) and
the maintainers will review and respond there.

- <opensource@tektronix.com> - For open-source policy and license questions.

## Contributing

Interested in contributing? Check out the [contributing guidelines](https://github.com/tektronix/python-package-ci-cd/blob/main/CONTRIBUTING.md). Please
note that this project is released with a [Code of Conduct](https://github.com/tektronix/python-package-ci-cd/blob/main/CODE_OF_CONDUCT.md). By
contributing to this project, you agree to abide by its terms.

## License

`python-package-ci-cd` was created by Tektronix. It is licensed under the terms of
the [Apache License 2.0](https://github.com/tektronix/python-package-ci-cd/blob/main/LICENSE.md).
