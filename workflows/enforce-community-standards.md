# enforce-community-standards.yml

This workflow will ensure that all necessary files are in place in order to meet the
Open Source Community Standards for a repository. The list of these files (and other settings) can
be found in the Community Standards section of the Insights tab of a public GitHub repository. You
can read about community profiles in
[GitHub's documentation](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories).

The full list of files that this workflow checks for is as follows:

- `.github/CODEOWNERS`
- `README.@(md|rst)`
- `CODE_OF_CONDUCT.@(md|rst)`
- `CONTRIBUTING.@(md|rst)`
- `LICENSE.@(md|rst)`
- `SECURITY.@(md|rst)`
- `.github/ISSUE_TEMPLATE/bug_report.@(yml|yaml)`
- `.github/ISSUE_TEMPLATE/feature_request.@(yml|yaml)`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/dependabot.@(yml|yaml)`
- `.github/workflows/codeql-analysis.@(yml|yaml)`

> [!NOTE]
> This workflow uses the following GitHub Actions:
>
> - [actions/checkout](https://github.com/actions/checkout)
> - [andstor/file-existence-action](https://github.com/andstor/file-existence-action)
> - [re-actors/alls-green](https://github.com/re-actors/alls-green)
>
> See the [Workflow file][workflow-file] for the currently used versions of each GitHub Action.

> [!TIP]
> See the [Workflow file][workflow-file] for implementation details.

## Example

```yaml
# .github/workflows/enforce-community-standards.yml
name: Enforce Open Source Community Standards
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  enforce-community-standards:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-enforce-community-standards.yml@v0.0.1
```

[workflow-file]: ../.github/workflows/_reusable-enforce-community-standards.yml
