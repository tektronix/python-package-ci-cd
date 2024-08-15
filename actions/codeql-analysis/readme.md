# codeql-analysis

This composite Action will checkout the code and then run a CodeQL analysis against the
provided languages in the repository. See the
[CodeQL docs](https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning/customizing-your-advanced-setup-for-code-scanning#changing-the-languages-that-are-analyzed)
for the complete list of supported languages.

## Inputs

| Input variable   | Necessity | Description                                        | Default                                |
| ---------------- | --------- | -------------------------------------------------- | -------------------------------------- |
| `language`       | required  | The language to analyze.                           |                                        |
| `codeql-queries` | optional  | A comma-separate list of CodeQL query sets to use. | security-extended,security-and-quality |

## Example

```yaml
# .github/workflows/codeql-analysis.yml
name: CodeQL
on:
  push:
    branches: [main]
jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write  # Allow CodeQL to create security events
    steps:
      - name: Run CodeQL Analysis
        uses: tektronix/python-package-ci-cd/actions/codeql-analysis@v0.1.0
        with:
          language: python  # required
          codeql-queries: security-extended,security-and-quality  # optional
```
