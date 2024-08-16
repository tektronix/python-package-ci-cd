# publish-api-comparison.yml

This workflow will use the output from the
[`check-api-for-breaking-changes.yml`](./check-api-for-breaking-changes.md) workflow to create a
comment on the Pull Request that introduces the changes with a detailed breakdown of the changes.
The reason this is a separate workflow that is triggered by the `workflow_run` event is to
allow Pull Requests from forks to still be commented on when there are breaking API changes. Due
to the reduced permissions of workflows that are run against Pull Requests from forks, this
workflow must be a separate workflow so that it has the elevated permissions necessary to
create a comment on the Pull Request.

The workflow calling this reusable workflow must be set to
trigger on a `completed` `workflow_run` event of the workflow that checks for API breaking
changes, usually a Workflow named `Check Public API for Breaking Changes`, see the
[example](#example) below for the correct yaml syntax.

> [!IMPORTANT]
> When calling this reusable workflow, the permissions must be set as follows:
>
> ```yaml
> permissions:
>   checks: write
>   pull-requests: write
> ```

## Example

```yaml
name: Publish API Breaking Change Check Results
on:
  workflow_run:
    workflows: [Check Public API for Breaking Changes]
    types: [completed]
jobs:
  publish-api-comparison:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-publish-api-comparison.yml@main  # it is recommended to use the latest release tag instead of `main`
    permissions:
      checks: write
      pull-requests: write
```
