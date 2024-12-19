# Contributing Guidelines

Contributions are welcome, and they are greatly appreciated! Every bit helps,
and credit will always be given.

## Types of Contributions

There are several types of contributions that can be made:

### Report Bugs

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Submit Feedback

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are
    welcome :)

## Get Started!

Ready to contribute? Here's how to set up `python-package-ci-cd` for local development.

> [!IMPORTANT]
> All commits going into the main repository are required to be signed, so make sure
> to set up commit signing before starting to make changes.

1. Set up commit signing, see [GitHub's documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification) for details.

2. Fork `python-package-ci-cd` into a new repository.

3. Set up a virtual environment and install the project with its dependencies:

    - Using the helper script (recommended):
        ```console
        python scripts/contributor_setup.py
        ```

4. Check to see if there are any [open issues](https://github.com/tektronix/python-package-ci-cd/issues) or [pull requests](https://github.com/tektronix/python-package-ci-cd/pulls) that are related to the change you wish to make.

5. Create or update an [issue](https://github.com/tektronix/python-package-ci-cd/issues) to track the status of your change.

6. Use `git` to create a branch for local development and make your changes:

    ```console
    git checkout -b name-of-your-bugfix-or-feature
    ```

7. Update the **Unreleased** section in the [CHANGELOG](./CHANGELOG.md) using the proper format.

8. When you're done making changes, check that your changes conform to any code
    formatting requirements.

    - To run the pre-commit checks (only after activating your virtual environment):

        ```console
        pre-commit run --all
        ```

9. Commit and push your changes, then open a pull request from
    the fork back into the main repository.

    - Commit messages must be structured as follows:
        ```
        <type>[optional scope]: <description>

        [optional body]

        [optional footer(s)]
        ```
    - `<type>` can be one of `fix`, `feat`, `build`, `ci`, `docs`, `style`,
        `refactor`, or `test`.
    - See the
        [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
        website for more details on this format.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. If the pull request adds functionality, the [README](./README.md) should be updated.
2. The **Unreleased** section in the [Changelog](./CHANGELOG.md) should be updated.

## Code of Conduct

Please note that the `python-package-ci-cd` project is released with a
[Code of Conduct](./CODE_OF_CONDUCT.md). By contributing to this project you agree
to abide by its terms.
