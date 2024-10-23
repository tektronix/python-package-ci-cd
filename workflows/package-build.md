# package-build.yml

This workflow will build the package using the
[`hynek/build-and-inspect-python-package`](https://github.com/hynek/build-and-inspect-python-package)
action, and then verify that the package can be installed on each combination of Python version
and operating system specified.

> [!NOTE]
> When building the Python package, this workflow will run in the `package-build` GitHub Actions environment.
> This environment will be created in the repository that calls this workflow. No additional setup is required.

> [!IMPORTANT]
> When calling this reusable workflow, the permissions must be set as follows:
>
> ```yaml
> permissions:
>   contents: read
>   id-token: write
>   attestations: write
> ```

> [!NOTE]
> This workflow uses concurrency to limit the number of builds that can run at the same time
> to a single build. For builds on the `main` branch, the workflow will simply create a queue.
> For builds on other branches (or builds triggered by Pull Requests), the workflow will cancel
> any currently running builds for the same branch (or Pull Request).

> [!NOTE]
> This workflow uses the following GitHub Actions:
>
> - [actions/checkout](https://github.com/actions/checkout)
> - [hynek/build-and-inspect-python-package](https://github.com/hynek/build-and-inspect-python-package)
> - [actions/download-artifact](https://github.com/actions/download-artifact)
> - [actions/setup-python](https://github.com/actions/setup-python)
> - [re-actors/alls-green](https://github.com/re-actors/alls-green)
>
> See the [Workflow file][workflow-file] for the currently used versions of each GitHub Action.

> [!TIP]
> See the [Workflow file][workflow-file] for implementation details.

## Inputs

| Input variable            | Necessity | Description                                                                                         | Default                            |
| ------------------------- | --------- | --------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `package-name`            | required  | The name of the package to build, install, and import (this must be the package's importable name). |                                    |
| `python-versions-array`   | required  | A valid JSON array of Python versions to validate the package can be installed with.                |                                    |
| `operating-systems-array` | optional  | A valid JSON array of operating system names to validate the package can be installed on.           | `'["ubuntu", "windows", "macos"]'` |

## Example

```yaml
name: Package Build
on:
  push:
    branches: [main]
    tags: ['*']
  pull_request:
    branches: [main]
# Cancel running jobs for the same workflow and branch.
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
jobs:
  package-build:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-package-build.yml@v1.5.0
    with:
      package-name: my_package  # required
      python-versions-array: '["3.9", "3.10", "3.11", "3.12"]'  # required
      operating-systems-array: '["ubuntu", "windows", "macos"]'  # optional
    permissions:
      contents: read
      id-token: write
      attestations: write
```

[workflow-file]: ../.github/workflows/_reusable-package-build.yml
