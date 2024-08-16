# publish-test-results.yml

This workflow will publish the test results from the `artifact_<operating-system-name>_tests` artifacts
uploaded by the [`test-code.yml`](./test-code.md) workflow by creating a
comment on the Pull Request that triggered the test run.
The reason this is a separate workflow that is triggered by the `workflow_run` event is to
allow Pull Requests from forks to still have test results published as comments. Due
to the reduced permissions of workflows that are run against Pull Requests from forks, this
workflow must be a separate workflow so that it has the elevated permissions necessary to
create a comment on the Pull Request.

In order to use this workflow, the following permissions must be set to
`write`: `checks` and `pull-requests`. The workflow calling this reusable workflow must be set to
trigger on a `completed` `workflow_run` event of the workflow that tests the code, usually a
Workflow named `Test code`.

## Inputs

> [!NOTE]
> The `operating_systems_array` input variable must match the `operating_systems_array` input
> variable that is used as an input to the `test-code.yml` workflow so that test results are
> published for each operating system that ran tests.

| Input variable            | Necessity | Description                                                               | Default                            |
| ------------------------- | --------- | ------------------------------------------------------------------------- | ---------------------------------- |
| `operating_systems_array` | required  | A valid JSON array of operating system names to publish test results for. | `'["ubuntu", "windows", "macos"]'` |

## Example

```yaml
name: Publish Test Results
on:
  workflow_run:
    workflows: [ Test code ]
    types: [ completed ]
jobs:
  publish-test-results:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-publish-test-results.yml@main  # it is recommended to use the latest release tag instead of `main`
    with:
        operating_systems_array: '["ubuntu", "windows", "macos"]'  # required
    permissions:
      checks: write
      pull-requests: write
```
