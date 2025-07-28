# PR Workflow Demo

## Overview
This repository demonstrates a GitHub Actions workflow that automates the creation of pull requests (PRs) when changes are pushed to a specific branch. The workflow streamlines the process of merging updates—such as automated image or dependency updates—by automatically opening a PR for review and merging.

## Workflow Logic
The workflow is defined in `.github/workflows/auto-pr-demo.yml` and operates as follows:

- **Trigger:** The workflow runs on every push to the `image-update` branch.
- **Job:** `pull-request`
  - **Environment:** Runs on the latest Ubuntu GitHub Actions runner.
  - **Steps:**
    1. **Checkout code:** Retrieves the repository code using `actions/checkout@v3`.
    2. **Expose commit data:** Extracts commit message subject and body as environment variables using `rlespinasse/git-commit-data-action@v1`.
    3. **Create Pull Request:** Uses `diillson/auto-pull-request@v1.0.1` to automatically create a pull request:
        - **Source branch:** `image-update`
        - **Destination branch:** `auto-pr-branch-create`
        - **Title/Body:** Populated from the commit message
        - **Label:** Adds an `auto-pr` label
        - **Reviewer:** Assigns a reviewer (can be customized)
        - **Allows empty PRs:** Yes (`pr_allow_empty: true` ensures a pull request is created even if there are no changes between the branches. This is useful for automation consistency, notifications, or triggering downstream processes that rely on the PR event, even when there are no file changes.)
        - **Authentication:** Uses a GitHub token stored in `secrets.GH_PAT`

## Project Concerns & Design Considerations
- **Automation:** Reduces manual effort by automatically creating PRs for updates, ensuring changes are reviewed before merging.
- **Consistency:** Standardizes the PR creation process for automated updates.
- **Security:** Uses a GitHub token for authentication and assigns a reviewer to ensure changes are reviewed.
- **Transparency:** All workflow actions and PRs are visible in the GitHub interface.
- **Extensibility:** The workflow can be modified to support additional branches, reviewers, or steps as needed.
- **Limitations:** The workflow assumes the presence of the `image-update` and `auto-pr-branch-create` branches and a valid `GH_PAT` secret.

## How to use this workflow
1. Ensure you have the branches `image-update` and `auto-pr-branch-create` in your repository.
2. Add a GitHub personal access token as a repository secret named `GH_PAT`.
3. Place the workflow file at `.github/workflows/auto-pr-demo.yml` (already present in this repo).
4. Push changes to the `image-update` branch to trigger the workflow and automatically open a PR to `auto-pr-branch-create`.

---
Feel free to customize the workflow file to fit your team's requirements or to add additional steps as needed.
