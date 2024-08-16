# sbom-scan.yml

This workflow will create a Software Bill of Materials (SBOM) for the repository using the
[`anchore/sbom-action`](https://github.com/anchore/sbom-action) Action and then scan the SBOM
using the [`anchore/scan-action`](https://github.com/anchore/scan-action) Action. It runs on the `ubuntu-latest` runner label,
uses the default version of Python available on the runner, and will use the latest compatible
version of [`poetry`](https://pypi.org/project/poetry/) to generate the lock file for the calling
repository's Python package.

In order to use this workflow, the Python package must be using the
[Poetry package manager](https://python-poetry.org/). When calling the reusable workflow, the
following permissions must be set to `write`: `security-events`, `contents`, `id-token`, and
`attestations`.

## Example

```yaml
name: Create & Scan SBOM
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  release:
    types: [published]
jobs:
  sbom-scan:
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-sbom-scan.yml@main  # it is recommended to use the latest release tag instead of `main`
    permissions:
      security-events: write
      contents: write
      id-token: write
      attestations: write
```
