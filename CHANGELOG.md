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

- Updated the `_reusable-package-build.yml` file to include a step that will test importing the built package to check for any missing dependencies.

### Changed

- Bumped dependency versions.

---

## v1.3.0 (2024-09-09)

### Merged Pull Requests

- Enhance find_unreleased_changelog_items action to check for merged PRs ([#74](https://github.com/tektronix/python-package-ci-cd/pull/74))
- Update package-release workflow to prevent marking the workflow as failed if the deployment is rejected ([#84](https://github.com/tektronix/python-package-ci-cd/pull/84))
- chore(gh-actions-deps): update hynek/build-and-inspect-python-package action to v2.9.0 in all dependant reusable workflows ([#83](https://github.com/tektronix/python-package-ci-cd/pull/83))
- chore(python-deps): update pydantic dependencies in all dependant actions ([#70](https://github.com/tektronix/python-package-ci-cd/pull/70))
- chore(python-deps): update dependency platformdirs to v4.3.2 in all dependant actions ([#82](https://github.com/tektronix/python-package-ci-cd/pull/82))
- chore(python-deps): update dependency more-itertools to v10.5.0 in all dependant actions ([#66](https://github.com/tektronix/python-package-ci-cd/pull/66))
- chore(python-deps): update dependency platformdirs to v4.3.1 in all dependant actions ([#80](https://github.com/tektronix/python-package-ci-cd/pull/80))
- chore(python-deps): update dependency virtualenv to v20.26.4 in all dependant actions ([#81](https://github.com/tektronix/python-package-ci-cd/pull/81))
- chore(python-deps): update dependency filelock to v3.16.0 in all dependant actions ([#79](https://github.com/tektronix/python-package-ci-cd/pull/79))
- chore(docker-deps): update python:3.12-alpine docker digest to bb5d0ac in all dependant actions ([#77](https://github.com/tektronix/python-package-ci-cd/pull/77))
- chore(python-deps): update dependency build to v1.2.2 in all dependant actions ([#76](https://github.com/tektronix/python-package-ci-cd/pull/76))
- test: Properly test the find_unreleased_changelog_items action ([#73](https://github.com/tektronix/python-package-ci-cd/pull/73))
- chore(gh-actions-deps): update actions/attest-build-provenance action to v1.4.3 in all dependant reusable workflows ([#72](https://github.com/tektronix/python-package-ci-cd/pull/72))
- ci: Add workflow to automatically approve renovate PRs that can be automerged to enable automatic updates of dependencies ([#71](https://github.com/tektronix/python-package-ci-cd/pull/71))
- Automate the release process trigger weekly ([#68](https://github.com/tektronix/python-package-ci-cd/pull/68))
- chore(gh-actions-deps): update python-semantic-release dependencies to v9.8.8 in all dependant reusable workflows ([#38](https://github.com/tektronix/python-package-ci-cd/pull/38))
- chore(python-deps): update dependency setuptools to v74.1.2 in all dependant actions ([#64](https://github.com/tektronix/python-package-ci-cd/pull/64))
- chore(python-deps): update dependency pypi-simple to v1.6.0 for actions/create_unique_testpypi_version and actions/update_development_dependencies ([#45](https://github.com/tektronix/python-package-ci-cd/pull/45))
- chore(python-deps): update dependency codespell to v2 for docs ([#57](https://github.com/tektronix/python-package-ci-cd/pull/57))
- chore(python-deps): update dependency poetry-plugin-export to v1.8.0 for actions/update_development_dependencies and dev ([#44](https://github.com/tektronix/python-package-ci-cd/pull/44))
- chore(python-deps): update dependency certifi to v2024.8.30 in all dependant actions ([#59](https://github.com/tektronix/python-package-ci-cd/pull/59))
- chore(docker-deps): update python:3.12-alpine docker digest to aeff643 in all dependant actions ([#50](https://github.com/tektronix/python-package-ci-cd/pull/50))
- chore(python-deps): update dependency rapidfuzz to v3.9.7 in all dependant actions ([#56](https://github.com/tektronix/python-package-ci-cd/pull/56))
- test: Test against macOS as well to catch any bugs when updating dependencies ([#58](https://github.com/tektronix/python-package-ci-cd/pull/58))
- chore(python-deps): update dependency cffi to v1.17.1 in all dependant actions ([#55](https://github.com/tektronix/python-package-ci-cd/pull/55))
- chore(gh-actions-deps): update actions/checkout action to v4.1.7 in all dependant reusable workflows ([#52](https://github.com/tektronix/python-package-ci-cd/pull/52))
- chore(python-deps): update dependency pyright to v1.1.379 for dev ([#49](https://github.com/tektronix/python-package-ci-cd/pull/49))
- chore(gh-actions-deps): update anchore/scan-action action to v4.1.2 in all dependant reusable workflows ([#53](https://github.com/tektronix/python-package-ci-cd/pull/53))
- chore(gh-actions-deps): update dev workflow dependencies ([#54](https://github.com/tektronix/python-package-ci-cd/pull/54))
- Update Renovate config ([#51](https://github.com/tektronix/python-package-ci-cd/pull/51))
- chore(docker-deps): pin python docker tag to c2f41e6 ([#37](https://github.com/tektronix/python-package-ci-cd/pull/37))
- chore(python-deps): update dependency tomli to v2.0.1 for the create_unique_testpypi_version group(s) ([#39](https://github.com/tektronix/python-package-ci-cd/pull/39))
- chore(config): migrate renovate config ([#42](https://github.com/tektronix/python-package-ci-cd/pull/42))
- chore: Configure Renovate ([#36](https://github.com/tektronix/python-package-ci-cd/pull/36))
- gh-actions(deps): Bump the gh-actions-dependencies group across 2 directories with 2 updates ([#33](https://github.com/tektronix/python-package-ci-cd/pull/33))
- fix: Check out the repo before trying to run local actions ([#34](https://github.com/tektronix/python-package-ci-cd/pull/34))
- Add comments with version numbers to the pinned versions of GitHub Actions in the reusable workflows ([#31](https://github.com/tektronix/python-package-ci-cd/pull/31))

### Added

- Added the ability for the `update_development_dependencies` action to accept a comma-separated, multiline string
- Added all PRs merged since the last release to the job summary for the release workflow

### Changed

- Bumped dependency versions.
- Changed the `_reusable-update-python-and-pre-commit-dependencies.yml` workflow to no longer only work on PRs from Dependabot, users will now need to apply any conditional login in the calling workflow.
- Updated the `_reusable-update-python-and-pre-commit-dependencies.yml` workflow to allow using [`renovate`](https://docs.renovatebot.com/) instead of Dependabot to update dependencies.
- Updated the `_reusable-package-release.yml` workflow to not show as failed if the `bump-release` deployment is rejected by a reviewer.
- Updated the `find_unreleased_changelog_items` action to check for merged PRs since the last release and fail if none are found.

---

## v1.2.0 (2024-08-30)

### Merged Pull Requests

- feat: Add an action that can be used to fetch a PR number ([#32](https://github.com/tektronix/python-package-ci-cd/pull/32))
- gh-actions(deps): Bump github/codeql-action ([#30](https://github.com/tektronix/python-package-ci-cd/pull/30))
- Build a documentation site with mkdocs to allow testing more reusable workflows ([#28](https://github.com/tektronix/python-package-ci-cd/pull/28))

### Added

- Added an action that can be used to fetch a PR number based on the `head_sha`.

### Changed

- Converted all references to third-party Actions used in Reusable Workflows from tags to SHAs to ensure that the workflows are stable and do not change unexpectedly.

---

## v1.1.1 (2024-08-28)

### Merged Pull Requests

- fix: Add a checkout step to make sure the python version can be determined from the pyproject.toml file ([#27](https://github.com/tektronix/python-package-ci-cd/pull/27))

### Fixed

- Fixed a bug in the `_reusable-package-testpypi.yml` workflow that prevented the package
    installation job from running properly by first performing a checkout of the repository
    before trying to read the `pyproject.toml` file in the repo to determine the correct Python version to use.

---

## v1.1.0 (2024-08-28)

### Merged Pull Requests

- fix: Allow the PyPI publishing workflows to be used as reusable workflows by requiring a token for uploading the package ([#26](https://github.com/tektronix/python-package-ci-cd/pull/26))
- ci: Update pre-commit hook to run properly without needing docker installed ([#25](https://github.com/tektronix/python-package-ci-cd/pull/25))
- docs: Fix changelog formatting ([#24](https://github.com/tektronix/python-package-ci-cd/pull/24))

### Changed

- Updated the `_reusable-package-testpypi.yml` and `_reusable-package-release.yml` workflows to use a token for uploading Python packages to TestPyPI and PyPI.

---

## v1.0.3 (2024-08-28)

### Merged Pull Requests

- fix: Removed duplicate step ID from reusable-package-testpypi.yml ([#23](https://github.com/tektronix/python-package-ci-cd/pull/23))
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
