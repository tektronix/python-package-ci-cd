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

> [!NOTE]
> This workflow uses the following GitHub Actions:
>
> - [dawidd6/action-download-artifact](https://github.com/dawidd6/action-download-artifact)
> - [8BitJonny/gh-get-current-pr](https://github.com/8BitJonny/gh-get-current-pr)
> - [marocchino/sticky-pull-request-comment](https://github.com/marocchino/sticky-pull-request-comment)
>
> See the [Workflow file][workflow-file] for the currently used versions of each GitHub Action.

> [!TIP]
> See the [Workflow file][workflow-file] for implementation details.

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

[workflow-file]: ../.github/workflows/_reusable-publish-api-comparison.yml
