# test-code.yml

This workflow will run the tests for the code in the repository that are defined by its
[`tox`](https://tox.wiki/en/stable/) configuration. The test results
(anything matching the `.results*/**` glob) and coverage data (matching the `.coverage*` glob)
will be uploaded as artifacts and code coverage results can optionally be uploaded to the Codecov application.

This workflow runs two categories of tox environments: a general category and a fast category. The
fast category is intended to run just the unit tests, while the general category should run a
more comprehensive set of linting, build checks, and tests. The general category needs to use the
[`tox-gh-actions`](https://pypi.org/project/tox-gh-actions/) Python package to be able to run
specific tox environments based on the installed Python version. The fast category runs the
`[testenv:tests]` tox environment and needs to use the
[`pytest-github-report`](https://pypi.org/project/pytest-github-report/) Python package in order
to create a markdown file that can be uploaded as an artifact and then used by the
[`publish-test-results.yml`](./publish-test-results.md) workflow to add comments to Pull Requests
that contain the test results.

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

> [!NOTE]
> This workflow uses concurrency to limit the number of builds that can run at the same time
> to a single build. For builds on the `main` branch, the workflow will simply create a queue.
> For builds on other branches (or builds triggered by Pull Requests), the workflow will cancel
> any currently running builds for the same branch (or Pull Request).

> [!NOTE]
> This workflow uses the following GitHub Actions:
>
> - [actions/checkout](https://github.com/actions/checkout)
> - [actions/setup-node](https://github.com/actions/setup-node)
> - [actions/setup-python](https://github.com/actions/setup-python)
> - [actions/upload-artifact](https://github.com/actions/upload-artifact)
> - [codecov/codecov-action](https://github.com/codecov/codecov-action)
> - [actions/download-artifact](https://github.com/actions/download-artifact)
> - [phoenix-actions/test-reporting](https://github.com/phoenix-actions/test-reporting)
> - [re-actors/alls-green](https://github.com/re-actors/alls-green)
>
> See the [Workflow file][workflow-file] for the currently used versions of each GitHub Action.

> [!TIP]
> See the [Workflow file][workflow-file] for implementation details.

## Inputs

| Input variable            | Necessity | Description                                                                                                                                                                                                                                     | Default                            |
| ------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `repo-name`               | required  | The full name of the repository to use to gate Codecov uploads, in the format `owner/repo`.                                                                                                                                                     |                                    |
| `python-versions-array`   | required  | A valid JSON array of Python versions to test against. A valid option is also the string 'pyproject.toml', indicating to use the defined Python version from the pyproject.toml file.                                                           |                                    |
| `operating-systems-array` | optional  | A valid JSON array of operating system names to run tests on.                                                                                                                                                                                   | `'["ubuntu", "windows", "macos"]'` |
| `upload-to-codecov`       | optional  | A boolean indicating if coverage results should be uploaded to Codecov.                                                                                                                                                                         | `false`                            |
| `enable-retry-os-array`   | optional  | A valid JSON array of operating system names where retries should be allowed. This only applies to the 'test-general' job matrix, and if an OS is provided that OS will receive 3 total attempts to successfully execute the 'tox run' command. | `'[]'`                             |

## Secrets

| Secret variable | Necessity | Description                                                                                                                         |
| --------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `codecov-token` | optional  | The token to use to upload coverage results to Codecov. Only required when the `upload-to-codecov` input variable is set to `true`. |

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
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-test-code.yml@v1.7.2
    with:
      repo-name: owner/repo  # required
      operating-systems-array: '["ubuntu", "windows", "macos"]'  # optional
      python-versions-array: '["3.9", "3.10", "3.11", "3.12"]'  # required
      upload-to-codecov: true  # optional
      enable-retry-os-array: '["macos"]'  # optional
    secrets:
      codecov-token: ${{ secrets.CODECOV_TOKEN }}  # optional
```

[workflow-file]: ../.github/workflows/_reusable-test-code.yml
