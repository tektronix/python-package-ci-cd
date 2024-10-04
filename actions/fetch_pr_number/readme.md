# fetch_pr_number

This action fetches the Pull Request number for the provided SHA in the provided GitHub repository.
See the [example](#example) below for usage details.

## Inputs

| Input variable      | Necessity | Description                                           | Default |
| ------------------- | --------- | ----------------------------------------------------- | ------- |
| `sha`               | required  | The SHA of the commit to find the PR number for.      |         |
| `github-repository` | required  | The GitHub repository to search for the PR in.        |         |
| `retry-delay`       | optional  | The delay in seconds between retries.                 | 120     |
| `max-attempts`      | optional  | The maximum number of attempts to find the PR number. | 5       |

## Outputs

| Output variable | Description    |
| --------------- | -------------- |
| `number`        | The PR number. |

## Example

```yaml
name: Publish Results
on:
  workflow_call:
jobs:
  publish-results:
    runs-on: ubuntu-latest
    steps:
      - uses: tektronix/python-package-ci-cd/actions/fetch_pr_number@v1.4.1
        id: fetch-pr-number
        with:
          sha: ${{ github.event.workflow_run.head_sha }}  # required
          github-repository: ${{ github.repository }}  # required
          retry-delay: 120  # optional
          max-attempts: 5  # optional
      - name: Echo PR Number
        run: |
          echo "PR Number: ${{ steps.fetch-pr-number.outputs.number }}"
```
