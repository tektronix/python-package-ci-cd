# sbom-scan.yml

This workflow will create a Software Bill of Materials (SBOM) for the repository using the
[`anchore/sbom-action`](https://github.com/anchore/sbom-action) Action and then scan the SBOM
using the [`anchore/scan-action`](https://github.com/anchore/scan-action) Action. It runs on the `ubuntu-latest` runner label,
uses the default version of Python available on the runner, and will use the latest compatible
version of [`poetry`](https://pypi.org/project/poetry/) to generate the lock file for the calling
repository's Python package.

> [!IMPORTANT]
> In order to use this workflow, the Python package must be using the
> [Poetry package manager](https://python-poetry.org/).

> [!IMPORTANT]
> When calling this reusable workflow, the permissions must be set as follows:
>
> ```yaml
> permissions:
>   security-events: write
>   contents: write
>   id-token: write
>   attestations: write
> ```

> [!NOTE]
> This workflow uses the following GitHub Actions:
>
> - [actions/checkout](https://github.com/actions/checkout)
> - [actions/setup-python](https://github.com/actions/setup-python)
> - [anchore/sbom-action](https://github.com/anchore/sbom-action)
> - [actions/attest-build-provenance](https://github.com/actions/attest-build-provenance)
> - [anchore/scan-action](https://github.com/anchore/scan-action)
> - [actions/upload-artifact](https://github.com/actions/upload-artifact)
> - [github/codeql-action/upload-sarif](https://github.com/github/codeql-action)
>
> See the [Workflow file][workflow-file] for the currently used versions of each GitHub Action.

> [!TIP]
> See the [Workflow file][workflow-file] for implementation details.

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
    uses: tektronix/python-package-ci-cd/.github/workflows/_reusable-sbom-scan.yml@v1.4.1
    permissions:
      security-events: write
      contents: write
      id-token: write
      attestations: write
```

[workflow-file]: ../.github/workflows/_reusable-sbom-scan.yml
