# .github

Org-wide defaults for `alterworld-hub`: reusable workflows, PR template, conventions.

Rules: [CONVENTIONS.md](CONVENTIONS.md).

## Reusable workflows

| Workflow | Does | Caller permissions |
|---|---|---|
| `pr-title.yml` | Validates PR title as a Conventional Commit | `pull-requests: read` |
| `secrets-scan.yml` | Scans the tree with gitleaks | `contents: read` |
| `release.yml` | Runs release-please; optionally moves major tag `vX` | `contents: write`, `pull-requests: write` |
| `container.yml` | Builds a multi-arch image, pushes to GHCR, returns digest | `contents: read`, `packages: write` |

## Usage

```yaml
jobs:
  pr-title:
    if: github.event_name == 'pull_request'
    uses: alterworld-hub/.github/.github/workflows/pr-title.yml@v0
    permissions:
      pull-requests: read
  image:
    uses: alterworld-hub/.github/.github/workflows/container.yml@v0
    permissions:
      contents: read
      packages: write
    with:
      push: ${{ github.event_name != 'pull_request' }}
```

Inputs and outputs: see the `on.workflow_call` block of each file.
