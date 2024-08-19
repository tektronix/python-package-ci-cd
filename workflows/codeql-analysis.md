# codeql-analysis.yml

This workflow will checkout the code and then run a CodeQL analysis against the
specified languages. See the
[CodeQL docs](https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning/customizing-your-advanced-setup-for-code-scanning#changing-the-languages-that-are-analyzed)
for the complete list of supported languages.

> [!IMPORTANT]
> When calling this reusable workflow, the permissions must be set as follows:
>
> ```yaml
> permissions:
>   actions: read
>   contents: read
>   security-events: write
> ```

> [!TIP]
> See the [Workflow file](../.github/workflows/_reusable-codeql-analysis.yml) for implementation details.

## Inputs

| Input variable    | Necessity | Description                                        | Default                                |
| ----------------- | --------- | -------------------------------------------------- | -------------------------------------- |
| `languages-array` | required  | A valid JSON array of languages to analyze.        |                                        |
| `codeql-queries`  | optional  | A comma-separate list of CodeQL query sets to use. | security-extended,security-and-quality |

## Example

```yaml
name: CodeQL
on:
  push:
    branches: [main]
jobs:
  analyze:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-codeql-analysis.yml@main  # it is recommended to use the latest release tag instead of `main`
    with:
      languages-array: '["python", "javascript"]'
      codeql-queries: security-extended,security-and-quality
    permissions:
      actions: read
      contents: read
      security-events: write
```
