# package-build.yml

This workflow will build the package using the
[`hynek/build-and-inspect-python-package`](https://github.com/hynek/build-and-inspect-python-package)
action, and then verify that the package can be installed on each combination of Python version
and operating system specified.

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

> [!TIP]
> See the [Workflow file](../.github/workflows/_reusable-package-build.yml) for implementation details.

## Inputs

| Input variable            | Necessity | Description                                                                               | Default                            |
| ------------------------- | --------- | ----------------------------------------------------------------------------------------- | ---------------------------------- |
| `package-name`            | required  | The name of the package to build and install.                                             |                                    |
| `python-versions-array`   | required  | A valid JSON array of Python versions to validate the package can be installed with.      |                                    |
| `operating-systems-array` | optional  | A valid JSON array of operating system names to validate the package can be installed on. | `'["ubuntu", "windows", "macos"]'` |

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
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-package-build.yml@main  # it is recommended to use the latest release tag instead of `main`
    with:
      package-name: my_package  # required
      python-versions-array: '["3.9", "3.10", "3.11", "3.12"]'  # required
      operating-systems-array: '["ubuntu", "windows", "macos"]'  # optional
    permissions:
      contents: read
      id-token: write
      attestations: write
```
