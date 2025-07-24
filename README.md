# PR Workflow Demo

## Overview
This repository demonstrates a GitHub workflow for reviewing and merging pull requests. The workflow is designed to be run on a GitHub Actions runner, and it includes the following steps:
1. **Checkout the code**: The workflow starts by checking out the code from the repository. This step is necessary to access the code that is being reviewed.
2. **Run tests**: The workflow runs the tes
3. **Review the code**: The workflow reviews the code changes made in the pull request. This step is where you can provide feedback on the code changes and make any necessary changes.
4. **Merge the pull request**: If the code changes are approved, the workflow merges the pull request into the main branch of the repository. This step is where the pull request is actually merged into the main branch.
5. **Close the pull request**: After the pull request is merged, the workflow closes the pull request. This step is where the pull request is closed and no longer visible to other users.
## How to use this workflow
To use this workflow, you need to create a new workflow file in your repository. The workflow file should be named `.github/workflows/pr-workflow.yml`. The workflow file should contain the following steps:
```yaml
name: PR Workflow Demo
on:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  pr-workflow:
    runs-on: ubuntu-latest
    steps:
