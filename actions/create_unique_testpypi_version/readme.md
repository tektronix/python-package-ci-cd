# create_unique_testpypi_version

This action creates a unique version number for the provided Python package to enable uploading
the package to [TestPyPI](https://test.pypi.org/).

It accomplishes this by creating a unique `.postN` version number. The unique version number is
written back to the `pyproject.toml` file in order to enable building the package with the
custom version number in a subsequent workflow step. This action currently only supports the
[Poetry package manager](https://python-poetry.org/).

This action is used in the [package-testpypi.yml](../../workflows/package-testpypi.md)
reusable workflow.

> [!IMPORTANT]
> This action requires that the `pyproject.toml` file exists in the current working directory.

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
      - uses: actions/checkout@692973e3d937129bcbf40652eb9f2f61becf3332
        with:
          fetch-depth: 0
      - uses: tektronix/python-package-ci-cd/actions/create_unique_testpypi_version@v1.5.2
        id: create-version
        with:
          package-name: my-package  # required
      - name: Build package
        uses: hynek/build-and-inspect-python-package@2dbbf2b252d3a3c7cec7a810e3ed5983bd17b13a
```
