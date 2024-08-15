|                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Code Quality** | [![CodeQL status](https://github.com/tektronix/python-package-ci-cd/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/tektronix/python-package-ci-cd/actions/workflows/codeql-analysis.yml) [![CodeFactor grade](https://www.codefactor.io/repository/github/tektronix/python-package-ci-cd/badge)](https://www.codefactor.io/repository/github/tektronix/python-package-ci-cd) [![pre-commit status](https://results.pre-commit.ci/badge/github/tektronix/python-package-ci-cd/main.svg)](https://results.pre-commit.ci/latest/github/tektronix/python-package-ci-cd/main) |

---

# GitHub Actions and Re-usable Workflows for Python Packaging CI/CD

`python-package-ci-cd` is a collection of GitHub Actions and re-usable Workflows that enable
Python Packaging CI/CD.

## Actions

- [`codeql-analysis`](./actions/codeql-analysis/readme.md)
    - This composite Action will checkout the code and then run a CodeQL analysis against the
        provided languages in the repository.

## Reusable Workflows

- [`check-api-for-breaking-changes.yml`](./workflows/check-api-for-breaking-changes.md)
    - This workflow will use the [`griffe`](https://mkdocstrings.github.io/griffe/) Python package to check for
        any major or breaking changes in a package's API.
- [`enforce-community-standards.yml`](./workflows/enforce-community-standards.md)
    - This workflow will ensure that all necessary files are in place in order to meet the
        Open Source Community Standards for a repository.
- [`publish-api-comparison.yml`](./workflows/publish-api-comparison.md)
    - This workflow will use the output from the
        [`check-api-for-breaking-changes.yml`](./workflows/check-api-for-breaking-changes.md) workflow to create a
        comment on the Pull Request that introduces the changes with a detailed breakdown of the changes.
- [`sbom-scan.yml`](./workflows/sbom-scan.md)
    - This workflow will create a Software Bill of Materials (SBOM) for the repository using the
        [`anchore/sbom-action`](https://github.com/anchore/sbom-action) Action and then scan the
        SBOM using the [`anchore/scan-action`](https://github.com/anchore/scan-action) Action.

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

Interested in contributing? Check out
the [contributing guidelines](https://github.com/tektronix/python-package-ci-cd/blob/main/CONTRIBUTING.md). Please
note that this project is released with
a [Code of Conduct](https://github.com/tektronix/python-package-ci-cd/blob/main/CODE_OF_CONDUCT.md). By
contributing to this project, you agree to abide by its terms.

## License

`python-package-ci-cd` was created by Tektronix. It is licensed under the terms of
the [Apache License 2.0](https://github.com/tektronix/python-package-ci-cd/blob/main/LICENSE.md).
