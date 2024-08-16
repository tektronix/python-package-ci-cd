# test-code.yml

This workflow will run the tests for the code in the repository that are defined by its
[`tox`](https://tox.readthedocs.io/en/latest/) configuration. The test results and coverage data
will be uploaded as artifacts and code coverage results can optionally be uploaded to the Codecov application.

This workflow runs two categories of tox environments: a general category and a fast category. The
fast category is intended to run just the unit tests, while the general category should run a
more comprehensive set of linting, build checks, and tests. The general category needs to use the
[`tox-gh-actions`](https://pypi.org/project/tox-gh-actions/) Python package to be able to run
specific tox environments based on the installed Python version. The fast category needs to use the
[`pytest-github-report`](https://pypi.org/project/pytest-github-report/) Python package in order
to create a markdown file that can be uploaded as an artifact and then used by the
[`publish-test-results.yml`](./publish-test-results.md) workflow to add comments to Pull Requests
that contain the test results.

In order for the Codecov upload to work, a `CODECOV_TOKEN` secret must be available to the
calling workflow, and secrets must be set to `inherit`.

See this sample tox configuration for an example of how to set up the tox environments so that
this workflow can be used. This example makes use of the following Python packages:

- Required to use this workflow:
    - [`tox`](https://pypi.org/project/tox/)
    - [`tox-gh-actions`](https://pypi.org/project/tox-gh-actions/)
    - [`pytest`](https://pypi.org/project/pytest/)
    - [`pytest-cov`](https://pypi.org/project/pytest-cov/)
    - [`pytest-html`](https://pypi.org/project/pytest-html/)
    - [`pytest-github-report`](https://pypi.org/project/pytest-github-report/)
- Used only in the example:
    - [`poetry`](https://pypi.org/project/poetry/)
    - [`twine`](https://pypi.org/project/twine/)
    - [`pre-commit`](https://pypi.org/project/pre-commit/)

```toml
# pyproject.toml
[tool.tox]
legacy_tox_ini = """
[tox]
requires = tox>4
isolated_build = True
envlist = py39,py310,py311,py312,tests

[gh-actions]
python =
    3.9: py39
    3.10: py310
    3.11: py311
    3.12: py312

[testenv]
package = wheel
deps =
    poetry
    twine
    pre-commit
    pytest
    pytest-cov
    pytest-html
commands_pre =
    poetry install --no-root --without=main
commands =
    !tests: poetry build --output=dist_{envname}
    !tests: twine check --strict dist_{envname}/*
    !tests: pre-commit run --all-files
    pytest -vv --showlocals --cov --junitxml={tox_root}/.results_{envname}/results.xml --cov-report=term --cov-report=xml:{tox_root}/.coverage_{envname}.xml --cov-report=html:{tox_root}/.results_{envname}/html --self-contained-html --html={tox_root}/.results_{envname}/results.html

[testenv:tests]
basepython = python
deps =
    pytest
    pytest-cov
    pytest-html
    pytest-github-report
passenv =
    pytest_report_title  # this is set by the test-code.yml workflow
setenv =
    pytest_github_report = true
    pytest_use_blanks = true
    GITHUB_STEP_SUMMARY = {tox_root}/.results_{envname}/github_report.md
commands_pre =
"""
```

## Inputs

| Input variable            | Necessity | Description                                                                                 | Default                            |
| ------------------------- | --------- | ------------------------------------------------------------------------------------------- | ---------------------------------- |
| `repo-name`               | required  | The full name of the repository to use to gate Codecov uploads, in the format `owner/repo`. |                                    |
| `operating-systems-array` | required  | A valid JSON array of operating system names to run tests on.                               | `'["ubuntu", "windows", "macos"]'` |
| `python-versions-array`   | required  | A valid JSON array of Python versions to test against.                                      |                                    |
| `upload-codecov`          | optional  | A boolean indicating if coverage results should be uploaded to Codecov.                     | `false`                            |

## Example

```yaml
name: Test code
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
# Cancel running jobs for the same workflow and branch.
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
jobs:
  test-code:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-test-code.yml@main  # it is recommended to use the latest release tag instead of `main`
    with:
      repo-name: owner/repo  # required
      operating-systems-array: '["ubuntu", "windows", "macos"]'  # required
      python-versions-array: '["3.9", "3.10", "3.11", "3.12"]'  # required
      upload-codecov: true  # optional
    secrets: inherit
```
