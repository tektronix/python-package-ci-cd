# test-docs.yml

This workflow will run the documentation tests for the code in the repository that are defined by its
[`tox`](https://tox.wiki/en/stable/) configuration. It will upload anything in the
`.results_<tox-env>/` folder as a workflow artifact by first compressing it into a .zip file to
reduce its size and then uploading the created .zip file.

> [!NOTE]
> This workflow runs on the `ubuntu-latest` runner and installs the latest version of
> `mermaid-cli` via `npm` and the latest version of `graphviz` via `apt`.

See this sample tox configuration for an example of how to set up the tox environments so that
this workflow can be used.

```toml
# pyproject.toml
[tool.tox]
legacy_tox_ini = """
[tox]
requires = tox>4
isolated_build = True
envlist = docs,doctests

[testenv]
package = wheel
setenv =
    DOC_PYTHON_VERSION = python3.11  # Keep this in sync with '.readthedocs.yml' and '.github/workflows/test-docs.yml'

[testenv:docs]  # this environment simply builds the documentation
basepython = {env:DOC_PYTHON_VERSION}
deps =
    mkdocs
commands =
    python -c "import shutil; shutil.rmtree('.results_{envname}', ignore_errors=True)"
    mkdocs --verbose build --site-dir .results_{envname}

[testenv:doctests]  # this environment builds the documentation, and then runs tests against it
basepython = {env:DOC_PYTHON_VERSION}
deps =
    pytest
    pytest-html
    mkdocs
commands =
    pytest -v -k "test_docs" --showlocals --junitxml={tox_root}/.results_{envname}/results.xml --self-contained-html --html={tox_root}/.results_{envname}/results.html
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
> - [thedoctor0/zip-release](https://github.com/thedoctor0/zip-release)
> - [actions/upload-artifact](https://github.com/actions/upload-artifact)
> - [re-actors/alls-green](https://github.com/re-actors/alls-green)
>
> See the [Workflow file][workflow-file] for the currently used versions of each GitHub Action.

> [!TIP]
> See the [Workflow file][workflow-file] for implementation details.

## Inputs

| Input variable   | Necessity | Description                                    | Default                  |
| ---------------- | --------- | ---------------------------------------------- | ------------------------ |
| `node-version`   | required  | The version of Node.js to install.             |                          |
| `python-version` | required  | The version of Python to install.              |                          |
| `tox-env-array`  | optional  | A valid JSON array of tox environments to run. | `'["docs", "doctests"]'` |

## Example

```yaml
name: Test docs
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
  test-docs:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-test-docs.yml@v1.2.0
    with:
      node-version: 20  # required
      python-version: '3.11'  # required
      tox-env-array: '["docs", "doctests"]'  # optional
```

[workflow-file]: ../.github/workflows/_reusable-test-docs.yml
