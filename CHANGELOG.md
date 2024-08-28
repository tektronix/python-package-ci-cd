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

---

## v1.0.3 (2024-08-28)

### Merged Pull Requests

- fix: Removed duplicate step ID from _reusable-package-testpypi.yml ([#23](https://github.com/tektronix/python-package-ci-cd/pull/23))
- docs: Fix URLs to point to the correct repository ([#22](https://github.com/tektronix/python-package-ci-cd/pull/22))

### Fixed

- Fixed the `_reusable-package-testpypi.yml` workflow by removing a duplicate step ID that caused the workflow to be unusable

---

## v1.0.2 (2024-08-27)

### Merged Pull Requests

- Update build script to properly add changed files to git during the release process ([#21](https://github.com/tektronix/python-package-ci-cd/pull/21))

### Fixed

- Actually fixed the issue with the semantic-release configuration preventing updated files with each new release version from being properly updated in the repo as a part of the release.

---

## v1.0.1 (2024-08-27)

### Merged Pull Requests

- docs: Update changelog with incoming change notes on python-semantic-release config updates ([#20](https://github.com/tektronix/python-package-ci-cd/pull/20))
- chore: Update all pinned versions of python-package-ci-cd to v1.0.0 ([#19](https://github.com/tektronix/python-package-ci-cd/pull/19))

### Fixed

- Fixed an issue with the semantic-release configuration preventing updated files with each new release version from being properly updated in the repo as a part of the release.

---

## v1.0.0 (2024-08-27)

### Added

- Added a reusable workflow to check the Python API for breaking changes: [`check-api-for-breaking-changes.yml`](./workflows/check-api-for-breaking-changes.md)
- Added a reusable workflow to perform CodeQL analysis: [`codeql-analysis.yml`](./workflows/codeql-analysis.md)
- Added a reusable workflow to enforce Open-Source community standards: [`enforce-community-standards.yml`](./workflows/enforce-community-standards.md)
- Added a reusable workflow to build a Python package: [`package-build.yml`](./workflows/package-build.md)
- Added a reusable workflow to upload a Python package to TestPyPI: [`package-testpypi.yml`](./workflows/package-testpypi.md)
- Added a reusable workflow to publish API comparison results as a Pull Request comment: [`publish-api-comparison.yml`](./workflows/publish-api-comparison.md)
- Added a reusable workflow to publish test results as a Pull Request comment: [`publish-test-results.yml`](./workflows/publish-test-results.md)
- Added a reusable workflow to create a Software Bill of Materials (SBOM) and scan it: [`sbom-scan.yml`](./workflows/sbom-scan.md)
- Added a reusable workflow to run tests and linting against Python package code: [`test-code.yml`](./workflows/test-code.md)
- Added a reusable workflow to run documentation builds and tests for a Python package: [`test-docs.yml`](./workflows/test-docs.md)
- Added a reusable workflow to update Python and `pre-commit` dependencies: [`update-python-and-pre-commit-dependencies.yml`](./workflows/update-python-and-pre-commit-dependencies.md)
