# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com), and this
project adheres to [Semantic Versioning](https://semver.org).

Valid subsections within a version are:

- Added
- Changed
- Deprecated
- Removed
- Fixed
- Security

---

## Unreleased

Things to be included in the next release go here.

### Added

- Added a reusable workflow to check the Python API for breaking changes: [`check-api-for-breaking-changes.yml`](./workflows/check-api-for-breaking-changes.md)
- Added a reusable workflow to perform CodeQL analysis: [`codeql-analysis.yml`](./workflows/codeql-analysis.md)
- Added a reusable workflow to enforce Open-Source community standards: [`enforce-community-standards.yml`](./workflows/enforce-community-standards.md)
- Added a reusable workflow to build a Python package: [`package-build.yml`](./workflows/package-build.md)
- Added a reusable workflow to publish a Python package to PyPI, GitHub Releases, and TestPyPI: [`package-release.yml`](./workflows/package-release.md)
- Added a reusable workflow to upload a Python package to TestPyPI: [`package-testpypi.yml`](./workflows/package-testpypi.md)
- Added a reusable workflow to publish API comparison results as a Pull Request comment: [`publish-api-comparison.yml`](./workflows/publish-api-comparison.md)
- Added a reusable workflow to publish test results as a Pull Request comment: [`publish-test-results.yml`](./workflows/publish-test-results.md)
- Added a reusable workflow to create a Software Bill of Materials (SBOM) and scan it: [`sbom-scan.yml`](./workflows/sbom-scan.md)
- Added a reusable workflow to run tests and linting against Python package code: [`test-code.yml`](./workflows/test-code.md)
- Added a reusable workflow to run documentation builds and tests for a Python package: [`test-docs.yml`](./workflows/test-docs.md)
- Added a reusable workflow to update Python and `pre-commit` dependencies: [`update-python-and-pre-commit-dependencies.yml`](./workflows/update-python-and-pre-commit-dependencies.md)
