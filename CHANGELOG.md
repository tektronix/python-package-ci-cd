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

### Changed

- Bumped dependency versions.

### Added

- Added GitHub annotations to the `check-api-for-breaking-changes` workflow to enable better visibility into any breaking changes detected. (see [#223](https://github.com/tektronix/python-package-ci-cd/issues/223))
- Updated the `package-release` workflow to not fail if there are no unreleased items, but instead to skip the release process. (see [#107](https://github.com/tektronix/python-package-ci-cd/issues/107))

---

## v1.5.3 (2024-12-04)

### Merged Pull Requests

- chore(gh-actions-deps): update dawidd6/action-download-artifact action to v7 in all dependant reusable workflows ([#259](https://github.com/tektronix/python-package-ci-cd/pull/259))
- chore(python-deps): update dependency mailbits to v0.2.2 in all dependant actions ([#258](https://github.com/tektronix/python-package-ci-cd/pull/258))
- chore(python-deps): update dependency fastjsonschema to v2.21.1 in all dependant actions ([#257](https://github.com/tektronix/python-package-ci-cd/pull/257))
- chore(python-deps): update dependency cryptography to v44 in all dependant actions ([#251](https://github.com/tektronix/python-package-ci-cd/pull/251))
- chore(python-deps): update dependency fastjsonschema to v2.21.0 in all dependant actions ([#252](https://github.com/tektronix/python-package-ci-cd/pull/252))
- chore(python-deps): update dependency tomli to v2.2.1 for actions/create_unique_testpypi_version and docs ([#254](https://github.com/tektronix/python-package-ci-cd/pull/254))
- docs: Remove section of contribution guide that duplicates a later section ([#256](https://github.com/tektronix/python-package-ci-cd/pull/256))
- chore(pre-commit-deps): pre-commit autoupdate ([#231](https://github.com/tektronix/python-package-ci-cd/pull/231))
- chore(python-deps): update dependency virtualenv to v20.28.0 in all dependant actions ([#249](https://github.com/tektronix/python-package-ci-cd/pull/249))
- chore(python-deps): update dependency pydantic to v2.10.2 in all dependant actions ([#250](https://github.com/tektronix/python-package-ci-cd/pull/250))
- chore(gh-actions-deps): update anchore/scan-action action to v5.3.0 in all dependant reusable workflows ([#247](https://github.com/tektronix/python-package-ci-cd/pull/247))
- chore(python-deps): update pydantic dependencies in all dependant actions ([#120](https://github.com/tektronix/python-package-ci-cd/pull/120))
- chore(python-deps): update dependency identify to v2.6.3 in all dependant actions ([#245](https://github.com/tektronix/python-package-ci-cd/pull/245))
- chore(python-deps): update dependency setuptools to v75.6.0 in all dependant actions ([#244](https://github.com/tektronix/python-package-ci-cd/pull/244))
- chore(gh-actions-deps): update actions/dependency-review-action action to v4.5.0 in dev workflows ([#242](https://github.com/tektronix/python-package-ci-cd/pull/242))
- chore(gh-actions-deps): update anchore/sbom-action action to v0.17.8 in all dependant reusable workflows ([#241](https://github.com/tektronix/python-package-ci-cd/pull/241))
- chore(python-deps): update dependency toml-sort to v0.24.2 for actions/update_development_dependencies ([#240](https://github.com/tektronix/python-package-ci-cd/pull/240))
- chore(python-deps): update dependency toml-sort to v0.24.1 for actions/update_development_dependencies ([#239](https://github.com/tektronix/python-package-ci-cd/pull/239))
- chore(gh-actions-deps): update codecov/codecov-action action to v5.0.7 in all dependant reusable workflows ([#238](https://github.com/tektronix/python-package-ci-cd/pull/238))
- chore(python-deps): update dependency toml-sort to v0.24.0 for actions/update_development_dependencies ([#237](https://github.com/tektronix/python-package-ci-cd/pull/237))
- chore(gh-actions-deps): update github/codeql-action action to v3.27.5 in all dependant reusable workflows ([#236](https://github.com/tektronix/python-package-ci-cd/pull/236))
- chore(gh-actions-deps): update codecov/codecov-action action to v5.0.2 in all dependant reusable workflows ([#235](https://github.com/tektronix/python-package-ci-cd/pull/235))
- chore(gh-actions-deps): update codecov/codecov-action action to v5.0.1 in all dependant reusable workflows ([#234](https://github.com/tektronix/python-package-ci-cd/pull/234))
- chore(gh-actions-deps): update codecov/codecov-action action to v5 in all dependant reusable workflows ([#233](https://github.com/tektronix/python-package-ci-cd/pull/233))
- chore(gh-actions-deps): update github/codeql-action action to v3.27.4 in all dependant reusable workflows ([#232](https://github.com/tektronix/python-package-ci-cd/pull/232))
- chore(python-deps): update dependency pyright to v1.1.389 for dev ([#230](https://github.com/tektronix/python-package-ci-cd/pull/230))
- chore(python-deps): update dependency setuptools to v75.4.0 in all dependant actions ([#226](https://github.com/tektronix/python-package-ci-cd/pull/226))
- chore(python-deps): update dependency tomli to v2.1.0 for actions/create_unique_testpypi_version and docs ([#227](https://github.com/tektronix/python-package-ci-cd/pull/227))
- chore(gh-actions-deps): update github/codeql-action action to v3.27.3 in all dependant reusable workflows ([#228](https://github.com/tektronix/python-package-ci-cd/pull/228))
- chore(python-deps): update dependency identify to v2.6.2 in all dependant actions ([#222](https://github.com/tektronix/python-package-ci-cd/pull/222))

### Changed

- Bumped dependency versions.

---

## v1.5.2 (2024-11-13)

### Merged Pull Requests

- chore: Update renovate config to include the new version of Python in the commit and Pull Request title ([#217](https://github.com/tektronix/python-package-ci-cd/pull/217))
- chore(python-deps): update dependency packaging to v24.2 in all dependant actions ([#211](https://github.com/tektronix/python-package-ci-cd/pull/211))
- Allow caller workflows to use pyproject.toml files as the source of the Python version ([#216](https://github.com/tektronix/python-package-ci-cd/pull/216))
- chore(python-deps): update dependency pyright to v1.1.388 for dev ([#214](https://github.com/tektronix/python-package-ci-cd/pull/214))
- Group Python version updates for Dockerfiles and pyproject.toml together ([#213](https://github.com/tektronix/python-package-ci-cd/pull/213))
- chore(gh-actions-deps): update github/codeql-action action to v3.27.1 in all dependant reusable workflows ([#212](https://github.com/tektronix/python-package-ci-cd/pull/212))
- chore(docker-deps): update python:3.12-alpine docker digest to 5049c05 in all dependant actions ([#210](https://github.com/tektronix/python-package-ci-cd/pull/210))
- chore(docker-deps): update python:3.12-alpine docker digest to 72d7e22 in all dependant actions ([#209](https://github.com/tektronix/python-package-ci-cd/pull/209))
- chore(docker-deps): update python:3.12-alpine docker digest to 45447e9 in all dependant actions ([#208](https://github.com/tektronix/python-package-ci-cd/pull/208))
- chore(docker-deps): update python:3.12-alpine docker digest to 18e32de in all dependant actions ([#207](https://github.com/tektronix/python-package-ci-cd/pull/207))
- chore(docker-deps): update python:3.12-alpine docker digest to edd1d85 in all dependant actions ([#206](https://github.com/tektronix/python-package-ci-cd/pull/206))
- chore(pre-commit-deps): pre-commit autoupdate ([#195](https://github.com/tektronix/python-package-ci-cd/pull/195))
- chore(gh-actions-deps): update actions/attest-build-provenance action to v1.4.4 in all dependant reusable workflows ([#200](https://github.com/tektronix/python-package-ci-cd/pull/200))
- chore(python-deps): update dependency cachecontrol to v0.14.1 in all dependant actions ([#199](https://github.com/tektronix/python-package-ci-cd/pull/199))
- chore(gh-actions-deps): update anchore/sbom-action action to v0.17.7 in all dependant reusable workflows ([#197](https://github.com/tektronix/python-package-ci-cd/pull/197))
- chore(gh-actions-deps): update anchore/scan-action action to v5.2.1 in all dependant reusable workflows ([#198](https://github.com/tektronix/python-package-ci-cd/pull/198))
- chore(gh-actions-deps): update hynek/build-and-inspect-python-package action to v2.10.0 in all dependant reusable workflows ([#196](https://github.com/tektronix/python-package-ci-cd/pull/196))
- chore(python-deps): update dependency pyright to v1.1.387 for dev ([#183](https://github.com/tektronix/python-package-ci-cd/pull/183))

### Added

- Added the ability for caller workflows for the `_reusable-test-docs.yml` and `_reusable-test-code.yml` workflows to specify to use the `pyproject.toml` file as the source of the Python version instead of always requiring a hard-coded Python version.

### Changed

- Bumped dependency versions.

---

## v1.5.1 (2024-11-04)

### Merged Pull Requests

- chore(gh-actions-deps): update actions/dependency-review-action action to v4.4.0 in dev workflows ([#191](https://github.com/tektronix/python-package-ci-cd/pull/191))
- chore(python-deps): update dependency pytest-cov to v6 for tests ([#194](https://github.com/tektronix/python-package-ci-cd/pull/194))
- chore(python-deps): update dependency setuptools to v75.3.0 in all dependant actions ([#192](https://github.com/tektronix/python-package-ci-cd/pull/192))
- chore(gh-actions-deps): update anchore/scan-action action to v5.2.0 in all dependant reusable workflows ([#193](https://github.com/tektronix/python-package-ci-cd/pull/193))
- chore(gh-actions-deps): update anchore/sbom-action action to v0.17.6 in all dependant reusable workflows ([#190](https://github.com/tektronix/python-package-ci-cd/pull/190))
- chore(python-deps): update dependency virtualenv to v20.27.1 in all dependant actions ([#189](https://github.com/tektronix/python-package-ci-cd/pull/189))
- chore(gh-actions-deps): update crazy-max/ghaction-import-gpg action to v6.2.0 in all dependant reusable workflows ([#188](https://github.com/tektronix/python-package-ci-cd/pull/188))
- chore(gh-actions-deps): update actions/setup-python action to v5.3.0 in all dependant reusable workflows ([#187](https://github.com/tektronix/python-package-ci-cd/pull/187))
- chore(python-deps): update dependency rapidfuzz to v3.10.1 in all dependant actions ([#186](https://github.com/tektronix/python-package-ci-cd/pull/186))
- chore(gh-actions-deps): update actions/setup-node action to v4.1.0 in all dependant reusable workflows ([#185](https://github.com/tektronix/python-package-ci-cd/pull/185))
- chore(pre-commit-deps): pre-commit autoupdate ([#184](https://github.com/tektronix/python-package-ci-cd/pull/184))
- chore(gh-actions-deps): update github/codeql-action action to v3.27.0 in all dependant reusable workflows ([#182](https://github.com/tektronix/python-package-ci-cd/pull/182))
- chore(gh-actions-deps): update anchore/scan-action action to v5.1.0 in all dependant reusable workflows ([#181](https://github.com/tektronix/python-package-ci-cd/pull/181))
- chore(gh-actions-deps): update anchore/sbom-action action to v0.17.5 in all dependant reusable workflows ([#179](https://github.com/tektronix/python-package-ci-cd/pull/179))
- chore(python-deps): update dependency pypi-simple to v1.6.1 for actions/create_unique_testpypi_version and actions/update_development_dependencies ([#178](https://github.com/tektronix/python-package-ci-cd/pull/178))
- chore(gh-actions-deps): update actions/cache action to v4.1.2 in all dependant reusable workflows ([#177](https://github.com/tektronix/python-package-ci-cd/pull/177))
- chore(gh-actions-deps): update actions/checkout action to v4.2.2 in all dependant reusable workflows ([#176](https://github.com/tektronix/python-package-ci-cd/pull/176))
- chore(python-deps): update dependency trove-classifiers to v2024.10.21.16 in all dependant actions ([#175](https://github.com/tektronix/python-package-ci-cd/pull/175))
- chore(python-deps): update dependency cryptography to v43.0.3 in all dependant actions ([#174](https://github.com/tektronix/python-package-ci-cd/pull/174))
- chore(gh-actions-deps): update dev workflow dependencies ([#173](https://github.com/tektronix/python-package-ci-cd/pull/173))

### Changed

- Bumped dependency versions.

---

## v1.5.0 (2024-10-23)

### Merged Pull Requests

- chore(python-deps): update dependency pre-commit to v4 for actions/update_development_dependencies and dev ([#145](https://github.com/tektronix/python-package-ci-cd/pull/145))
- chore(gh-actions-deps): update anchore/scan-action action to v5 in all dependant reusable workflows ([#169](https://github.com/tektronix/python-package-ci-cd/pull/169))
- chore(python-deps): update dependency virtualenv to v20.27.0 in all dependant actions ([#172](https://github.com/tektronix/python-package-ci-cd/pull/172))
- chore(python-deps): update dependency setuptools to v75.2.0 in all dependant actions ([#165](https://github.com/tektronix/python-package-ci-cd/pull/165))
- chore(python-deps): update dependency tomli-w to v1.1.0 for actions/create_unique_testpypi_version ([#166](https://github.com/tektronix/python-package-ci-cd/pull/166))
- chore(python-deps): update poetry dependencies in all dependant actions ([#171](https://github.com/tektronix/python-package-ci-cd/pull/171))
- chore(python-deps): update dependency charset-normalizer to v3.4.0 in all dependant actions ([#164](https://github.com/tektronix/python-package-ci-cd/pull/164))
- chore(python-deps): update dependency trove-classifiers to v2024.10.16 in all dependant actions ([#167](https://github.com/tektronix/python-package-ci-cd/pull/167))
- chore: Group all poetry dependencies together when updating dependencies ([#170](https://github.com/tektronix/python-package-ci-cd/pull/170))
- chore(python-deps): update dependency pyright to v1.1.385 for dev ([#162](https://github.com/tektronix/python-package-ci-cd/pull/162))
- chore(python-deps): update dependency build to v1.2.2.post1 in all dependant actions ([#146](https://github.com/tektronix/python-package-ci-cd/pull/146))
- chore(gh-actions-deps): update anchore/sbom-action action to v0.17.4 in all dependant reusable workflows ([#155](https://github.com/tektronix/python-package-ci-cd/pull/155))
- Enable skipping pre-commit hook repos during development dependency update workflow and action ([#158](https://github.com/tektronix/python-package-ci-cd/pull/158))
- chore(python-deps): update dependency distlib to v0.3.9 in all dependant actions ([#157](https://github.com/tektronix/python-package-ci-cd/pull/157))
- chore(gh-actions-deps): update actions/upload-artifact action to v4.4.3 in all dependant reusable workflows ([#149](https://github.com/tektronix/python-package-ci-cd/pull/149))
- chore(python-deps): update dependency pkginfo to v1.11.2 in all dependant actions ([#159](https://github.com/tektronix/python-package-ci-cd/pull/159))
- chore(gh-actions-deps): update actions/checkout action to v4.2.1 in dev workflows ([#148](https://github.com/tektronix/python-package-ci-cd/pull/148))
- chore(docker-deps): update python:3.12-alpine docker digest to 38e179a in all dependant actions ([#153](https://github.com/tektronix/python-package-ci-cd/pull/153))
- chore(gh-actions-deps): update actions/cache action to v4.1.1 in all dependant reusable workflows ([#154](https://github.com/tektronix/python-package-ci-cd/pull/154))
- chore(gh-actions-deps): update actions/checkout action to v4.2.1 in all dependant reusable workflows ([#147](https://github.com/tektronix/python-package-ci-cd/pull/147))
- chore(gh-actions-deps): update github/codeql-action action to v3.26.13 in all dependant reusable workflows ([#150](https://github.com/tektronix/python-package-ci-cd/pull/150))
- Install LTS node during reusable testing workflow ([#152](https://github.com/tektronix/python-package-ci-cd/pull/152))
- chore(gh-actions-deps): update actions/cache action to v4.1.0 in all dependant reusable workflows ([#144](https://github.com/tektronix/python-package-ci-cd/pull/144))
- chore(gh-actions-deps): update github/codeql-action action to v3.26.11 in all dependant reusable workflows ([#143](https://github.com/tektronix/python-package-ci-cd/pull/143))
- chore(pre-commit-deps): pre-commit autoupdate ([#142](https://github.com/tektronix/python-package-ci-cd/pull/142))
- chore(python-deps): update dependency tomli to v2.0.2 for actions/create_unique_testpypi_version and docs ([#140](https://github.com/tektronix/python-package-ci-cd/pull/140))
- chore(gh-actions-deps): update codecov/codecov-action action to v4.6.0 in all dependant reusable workflows ([#139](https://github.com/tektronix/python-package-ci-cd/pull/139))
- chore(gh-actions-deps): update github/codeql-action action to v3.26.10 in all dependant reusable workflows ([#138](https://github.com/tektronix/python-package-ci-cd/pull/138))
- docs: Update changelog to address mdformat issues ([#137](https://github.com/tektronix/python-package-ci-cd/pull/137))

### Added

- Added a new `pre-commit-repo-update-skip-list` input parameter to the `update_development_dependencies` action and the `_reusable-update-python-and-pre-commit-dependencies.yml` workflow to allow users to skip updating specific `pre-commit` hooks.

### Changed

- Bumped dependency versions.

---

## v1.4.1 (2024-10-04)

### Merged Pull Requests

- chore(python-deps): update dependency pyproject-hooks to v1.2.0 in all dependant actions ([#136](https://github.com/tektronix/python-package-ci-cd/pull/136))
- chore(python-deps): update dependency pyright to v1.1.383 for dev ([#135](https://github.com/tektronix/python-package-ci-cd/pull/135))
- chore(gh-actions-deps): update python-semantic-release/python-semantic-release action to v9.9.0 in all dependant reusable workflows ([#134](https://github.com/tektronix/python-package-ci-cd/pull/134))
- chore(gh-actions-deps): update python-semantic-release/python-semantic-release action to v9.8.9 in all dependant reusable workflows ([#131](https://github.com/tektronix/python-package-ci-cd/pull/131))
- chore(gh-actions-deps): update actions/checkout action to v4.2.0 in all dependant reusable workflows ([#126](https://github.com/tektronix/python-package-ci-cd/pull/126))
- chore(python-deps): update dependency virtualenv to v20.26.6 in all dependant actions ([#133](https://github.com/tektronix/python-package-ci-cd/pull/133))
- chore(gh-actions-deps): update actions/checkout action to v4.2.0 in dev workflows ([#127](https://github.com/tektronix/python-package-ci-cd/pull/127))
- chore(python-deps): update dependency pyright to v1.1.382.post1 for dev ([#132](https://github.com/tektronix/python-package-ci-cd/pull/132))
- chore(docker-deps): update python:3.12-alpine docker digest to e75de17 in all dependant actions ([#130](https://github.com/tektronix/python-package-ci-cd/pull/130))
- chore(docker-deps): update python:3.12-alpine docker digest to 6666ea3 in all dependant actions ([#129](https://github.com/tektronix/python-package-ci-cd/pull/129))
- chore(pre-commit-deps): pre-commit autoupdate ([#117](https://github.com/tektronix/python-package-ci-cd/pull/117))
- chore(python-deps): update dependency pyright to v1.1.382.post0 for dev ([#125](https://github.com/tektronix/python-package-ci-cd/pull/125))
- chore(python-deps): update dependency pyright to v1.1.382 for dev ([#124](https://github.com/tektronix/python-package-ci-cd/pull/124))
- chore(gh-actions-deps): update github/codeql-action action to v3.26.9 in all dependant reusable workflows ([#123](https://github.com/tektronix/python-package-ci-cd/pull/123))
- chore(python-deps): update dependency rapidfuzz to v3.10.0 in all dependant actions ([#122](https://github.com/tektronix/python-package-ci-cd/pull/122))
- Update automerge of pre-commit to use the squash strategy ([#121](https://github.com/tektronix/python-package-ci-cd/pull/121))
- chore(gh-actions-deps): update actions/setup-node action to v4.0.4 in all dependant reusable workflows ([#119](https://github.com/tektronix/python-package-ci-cd/pull/119))
- chore(gh-actions-deps): update github/codeql-action action to v3.26.8 in all dependant reusable workflows ([#118](https://github.com/tektronix/python-package-ci-cd/pull/118))
- chore(python-deps): update dependency pyright to v1.1.381 for dev ([#116](https://github.com/tektronix/python-package-ci-cd/pull/116))
- chore(python-deps): update dependency virtualenv to v20.26.5 in all dependant actions ([#115](https://github.com/tektronix/python-package-ci-cd/pull/115))
- chore(python-deps): update dependency platformdirs to v4.3.6 in all dependant actions ([#113](https://github.com/tektronix/python-package-ci-cd/pull/113))
- chore(python-deps): update dependency filelock to v3.16.1 in all dependant actions ([#114](https://github.com/tektronix/python-package-ci-cd/pull/114))
- chore(python-deps): update pydantic dependencies in all dependant actions ([#112](https://github.com/tektronix/python-package-ci-cd/pull/112))
- chore(python-deps): update dependency setuptools to v75 in all dependant actions ([#111](https://github.com/tektronix/python-package-ci-cd/pull/111))
- chore(python-deps): update dependency idna to v3.10 in all dependant actions ([#110](https://github.com/tektronix/python-package-ci-cd/pull/110))
- chore(python-deps): update dependency setuptools to v74.1.3 in all dependant actions ([#108](https://github.com/tektronix/python-package-ci-cd/pull/108))
- chore(python-deps): update dependency identify to v2.6.1 in all dependant actions ([#106](https://github.com/tektronix/python-package-ci-cd/pull/106))
- chore(python-deps): update dependency idna to v3.9 in all dependant actions ([#104](https://github.com/tektronix/python-package-ci-cd/pull/104))
- chore(python-deps): update dependency trove-classifiers to v2024.9.12 in all dependant actions ([#105](https://github.com/tektronix/python-package-ci-cd/pull/105))
- Enable automerge for pre commit hook updates ([#102](https://github.com/tektronix/python-package-ci-cd/pull/102))
- chore(python-deps): update dependency platformdirs to v4.3.3 in all dependant actions ([#103](https://github.com/tektronix/python-package-ci-cd/pull/103))
- chore(gh-actions-deps): update github/codeql-action action to v3.26.7 in all dependant reusable workflows ([#101](https://github.com/tektronix/python-package-ci-cd/pull/101))
- chore(python-deps): update dependency urllib3 to v2.2.3 in all dependant actions ([#98](https://github.com/tektronix/python-package-ci-cd/pull/98))
- chore(python-deps): update dependency pyright to v1.1.380 for dev ([#96](https://github.com/tektronix/python-package-ci-cd/pull/96))
- chore(python-deps): update dependency msgpack to v1.1.0 in all dependant actions ([#95](https://github.com/tektronix/python-package-ci-cd/pull/95))
- chore(docker-deps): update python:3.12-alpine docker digest to 7130f75 in all dependant actions ([#94](https://github.com/tektronix/python-package-ci-cd/pull/94))

### Changed

- Bumped dependency versions.

---

## v1.4.0 (2024-09-11)

### Merged Pull Requests

- feat: Enable importing the built package during the `package-build` workflow ([#93](https://github.com/tektronix/python-package-ci-cd/pull/93))
- ci: Update the automated release schedule to trigger a patch release on the 4th of every month ([#90](https://github.com/tektronix/python-package-ci-cd/pull/90))
- chore(docker-deps): update python:3.12-alpine docker digest to e0e4d3d in all dependant actions ([#89](https://github.com/tektronix/python-package-ci-cd/pull/89))
- ci: Allow automatic merging of digest updates ([#88](https://github.com/tektronix/python-package-ci-cd/pull/88))
- ci: Automatically approve pre-commit-ci autoupdate PRs ([#86](https://github.com/tektronix/python-package-ci-cd/pull/86))

### Added

- Updated the `_reusable-package-build.yml` file to include a step that will test importing the built package to check for any missing dependencies.
    - IMPORTANT: This workflow now requires the `package-name` input be the python-importable name of the package to be built, e.g. `python -c "import package_name"`.

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
