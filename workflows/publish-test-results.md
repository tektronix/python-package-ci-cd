# publish-test-results.yml

This workflow will publish the test results from the `artifact_<operating-system-name>_tests` artifacts
uploaded by the [`test-code.yml`](./test-code.md) workflow by creating a
comment on the Pull Request that triggered the test run.
The reason this is a separate workflow that is triggered by the `workflow_run` event is to
allow Pull Requests from forks to still have test results published as comments. Due
to the reduced permissions of workflows that are run against Pull Requests from forks, this
workflow must be a separate workflow so that it has the elevated permissions necessary to
create a comment on the Pull Request.

The workflow calling this reusable workflow must be set to
trigger on a `completed` `workflow_run` event of the workflow that tests the code, usually a
Workflow named `Test code`, see the [example](#example) below for the correct yaml syntax.

> [!IMPORTANT]
> When calling this reusable workflow, the permissions must be set as follows:
>
> ```yaml
> permissions:
>   checks: write
>   pull-requests: write
> ```

> [!NOTE]
> This workflow uses the following GitHub Actions:
>
> - [dawidd6/action-download-artifact](https://github.com/dawidd6/action-download-artifact)
> - [tektronix/python-package-ci-cd/actions/fetch_pr_number](https://github.com/tektronix/python-package-ci-cd)
>   - [actions/github-script](https://github.com/actions/github-script)
> - [marocchino/sticky-pull-request-comment](https://github.com/marocchino/sticky-pull-request-comment)
>
> See the [Workflow file][workflow-file] for the currently used versions of each GitHub Action.

> [!TIP]
> See the [Workflow file][workflow-file] for implementation details.

## Inputs

> [!IMPORTANT]
> The `operating-systems-array` input variable must match the `operating-systems-array` input
> variable that is used as an input to the `test-code.yml` workflow so that test results are
> published for each operating system that ran tests.

| Input variable            | Necessity | Description                                                               | Default                            |
| ------------------------- | --------- | ------------------------------------------------------------------------- | ---------------------------------- |
| `operating-systems-array` | optional  | A valid JSON array of operating system names to publish test results for. | `'["ubuntu", "windows", "macos"]'` |

## Example

```yaml
name: Publish Test Results
on:
  workflow_run:
    workflows: [Test code]
    types: [completed]
jobs:
  publish-test-results:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-publish-test-results.yml@v1.7.3
    with:
        operating-systems-array: '["ubuntu", "windows", "macos"]'  # required
    permissions:
      checks: write
      pull-requests: write
```

[workflow-file]: ../.github/workflows/_reusable-publish-test-results.yml
