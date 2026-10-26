# .github

Org-wide defaults for `alterworld-hub`: reusable workflows, PR template, conventions.

Rules: [CONVENTIONS.md](CONVENTIONS.md).

## Reusable workflows

| Workflow | Does | Caller permissions |
|---|---|---|
| `service.yml` | Full service pipeline (below). Use this. | `contents: write`, `pull-requests: write`, `packages: write` |
| `pr-title.yml` | PR title is a Conventional Commit; body references an issue (bots exempt; after editing the body, re-run) | `pull-requests: read` |
| `secrets-scan.yml` | gitleaks over the tree | `contents: read` |
| `container.yml` | Build multi-arch image; push `sha-<short>`; output digest | `contents: read`, `packages: write` |
| `release.yml` | release-please; optional major tag `vX` | `contents: write`, `pull-requests: write` |
| `promote.yml` | Release artifact: image `sha-<source-sha>` (waits for it) tagged `X.Y.Z`, `X.Y`; chart at release commit with digest baked in, pushed to `oci://ghcr.io/alterworld-hub/charts/<name>:X.Y.Z` | `contents: read`, `packages: write` |
| `gitops-bump.yml` | PR in `gitops`: set `<app>` release on nodes; auto-merge | none (uses bot token) |

`service.yml`:
- PR: pr-title, secrets-scan, image build (no push).
- `main`: secrets-scan, image push `sha-<short>`, release-please.
- Release commit: no image build. Promote the image of its parent (the `main` commit that was built and checked) to `X.Y.Z`; same digest as `sha-<parent>`.
- Then: bot PR in `gitops` setting the chart version in `nodes/<node>/apps/<app>.version.yaml` for `deploy-nodes` (default `local`), auto-merged when checks pass. One value per node = atomic rollout (chart pins the image).

## Org automation (runs in this repo)
- `project-sync.yml`: every 15 min, keeps [project #2](https://github.com/orgs/alterworld-hub/projects/2) consistent (`scripts/project-sync.py`). Manual run with `dry-run` prints actions only.
- `renovate.yml`: daily, self-hosted Renovate as the bot for all org repos (`renovate/config.json`): third-party charts (via `# renovate:` hints in gitops), base images, npm, actions, tool images. Own artifacts excluded (gitops-bump). Manual run with `dry-run`.
- Issue forms (`.github/ISSUE_TEMPLATE`): default for every org repo without its own; set issue type and add to the project.

## Service `ci.yml`

```yaml
name: ci
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
permissions: {}
jobs:
  check:            # language-specific: lint, test, build
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: read
    steps: [...]
  service:
    needs: check
    uses: alterworld-hub/.github/.github/workflows/service.yml@v0
    permissions:
      contents: write
      pull-requests: write
      packages: write
    secrets:
      BOT_PRIVATE_KEY: ${{ secrets.BOT_PRIVATE_KEY }}
```

Org secret `BOT_PRIVATE_KEY` = private key of GitHub App `alterworld-hub-bot`. release-please acts as the bot so release PRs trigger CI.

## Bot app `alterworld-hub-bot`
Installed on all org repos ([installation](https://github.com/organizations/alterworld-hub/settings/installations/175553363)). Used by release-please, gitops-bump, project-sync, Renovate.

| Permission | Access | Why |
|---|---|---|
| Contents | write | release commits and tags, Renovate and gitops-bump branches |
| Pull requests | write | release, Renovate and gitops-bump PRs; auto-merge |
| Issues | write | release-please labels, Renovate dashboard, project-sync closes epics |
| Organization projects | write | project-sync edits project #2 |
| Workflows | write | Renovate updates action pins in `.github/workflows` |
| Commit statuses | write | Renovate `renovate/stability-days` status |
| Dependabot alerts | read | Renovate vulnerability alerts |
| Metadata | read | mandatory |

Changing permissions in the app settings does not apply them: the org owner must accept the new permissions on the installation page. Until then the token keeps the old set (symptom: 403 / "Resource not accessible by integration").

Required checks for `main`: `check`, `service / image / build`, `service / pr-title / check`, `service / secrets-scan / gitleaks`.

## Build speed rules
- No `RUN` under emulation. Arch-independent output (JS): build stage `FROM --platform=$BUILDPLATFORM`. Binaries (Rust): cross-compile or native arm64 runners. `qemu: true` only as last resort.
- `cache-mode: min` by default; `max` only when rebuilding layers costs more than exporting them (e.g. Rust deps).
