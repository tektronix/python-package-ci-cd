|                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Code Quality** | [![CodeQL status](https://github.com/tektronix/python-package-ci-cd/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/tektronix/python-package-ci-cd/actions/workflows/codeql-analysis.yml) [![CodeFactor grade](https://www.codefactor.io/repository/github/tektronix/python-package-ci-cd/badge)](https://www.codefactor.io/repository/github/tektronix/python-package-ci-cd) [![pre-commit status](https://results.pre-commit.ci/badge/github/tektronix/python-package-ci-cd/main.svg)](https://results.pre-commit.ci/latest/github/tektronix/python-package-ci-cd/main) |

---

# GitHub Actions and Re-usable Workflows for Python Packaging CI/CD

`python-package-ci-cd` is a collection of GitHub Actions and re-usable Workflows that enable
Python Packaging CI/CD.

## Actions

- [`update-development-dependencies`](./actions/update-development-dependencies/readme.md)
    - This action enables updating Python development dependencies using the
        [`Poetry`](https://python-poetry.org/) package manager in-sync with
        [`pre-commit`](https://pre-commit.com/) hooks.

## Reusable Workflows

- [`check-api-for-breaking-changes.yml`](./workflows/check-api-for-breaking-changes.md)
    - This workflow will use the [`griffe`](https://mkdocstrings.github.io/griffe/) Python package to check for
        any major or breaking changes in a package's API.
- [`codeql-analysis.yml`](./workflows/codeql-analysis.md)
    - This workflow will checkout the code and then run a CodeQL analysis against the
        specified languages.
- [`enforce-community-standards.yml`](./workflows/enforce-community-standards.md)
    - This workflow will ensure that all necessary files are in place in order to meet the
        Open Source Community Standards for a repository.
- [`package-build.yml`](./workflows/package-build.md)
    - This workflow will build the package using the
        [`hynek/build-and-inspect-python-package`](https://github.com/hynek/build-and-inspect-python-package)
        action, and then verify that the package can be installed on each combination of Python version
        and operating system specified.
- [`package-testpypi.yml`](./workflows/package-testpypi.md)
    - This workflow will build the package using the
        [`hynek/build-and-inspect-python-package`](https://github.com/hynek/build-and-inspect-python-package)
        action, upload the package to [TestPyPI](https://test.pypi.org), and then verify that the package
        can be installed from [TestPyPI](https://test.pypi.org).
- [`publish-api-comparison.yml`](./workflows/publish-api-comparison.md)
    - This workflow will use the output from the
        [`check-api-for-breaking-changes.yml`](./workflows/check-api-for-breaking-changes.md) workflow to create a
        comment on the Pull Request that introduces the changes with a detailed breakdown of the changes.
- [`publish-test-results.yml`](./workflows/publish-test-results.md)
    - This workflow will publish the test results from the `artifact_<operating-system-name>_tests` artifacts
        uploaded by the [`test-code.yml`](./workflows/test-code.md) workflow by creating a
        comment on the Pull Request that triggered the test run.
- [`sbom-scan.yml`](./workflows/sbom-scan.md)
    - This workflow will create a Software Bill of Materials (SBOM) for the repository using the
        [`anchore/sbom-action`](https://github.com/anchore/sbom-action) Action and then scan the
        SBOM using the [`anchore/scan-action`](https://github.com/anchore/scan-action) Action.
- [`test-code.yml`](./workflows/test-code.md)
    - This workflow will run the tests for the code in the repository that are defined by its
        [`tox`](https://tox.wiki/en/stable/) configuration.
- [`test-docs.yml`](./workflows/test-docs.md)
    - This workflow will run the documentation tests for the code in the repository that are defined by its
        [`tox`](https://tox.wiki/en/stable/) configuration.
- [`update-python-and-pre-commit-dependencies.yml`](./workflows/update-python-and-pre-commit-dependencies.md)
    - This workflow updates Python development dependencies using the
        [`Poetry`](https://python-poetry.org/) package manager in-sync with
        [`pre-commit`](https://pre-commit.com/) hooks when triggered as a part of
        [`Dependabot`](https://docs.github.com/en/code-security/getting-started/dependabot-quickstart-guide)
        updates for the Python dependencies.

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
