# create-unique-testpypi-version

This action creates a unique version number for the provided Python package to enable uploading
the package to [TestPyPI](https://test.pypi.org/).

It accomplishes this by creating a unique `.postN` version number. The unique version number is
written back to the `pyproject.toml` file in order to enable building the package with the
custom version number in a subsequent workflow step. This action currently only supports the
[Poetry package manager](https://python-poetry.org/).

This action is used in the [package-testpypi.yml](../../workflows/package-testpypi.md)
reusable workflow.

## Inputs

| Input variable | Necessity | Description                                             | Default |
| -------------- | --------- | ------------------------------------------------------- | ------- |
| `package-name` | required  | The name of the package to create a unique version for. |         |

## Outputs

| Output variable | Description                                     |
| --------------- | ----------------------------------------------- |
| `new-version`   | The new version number created for the package. |

## Example

```yaml
jobs:
  test-pypi-build:
    name: Build package with unique version for test.pypi.org
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: ./actions/create-unique-testpypi-version
        id: create-version
        with:
          package-name: my-package  # required
      - name: Build package
        uses: hynek/build-and-inspect-python-package@v2.8.0
```
