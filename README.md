# .github

Org-wide defaults for `alterworld-hub`: reusable workflows, PR template, conventions.

Rules: [CONVENTIONS.md](CONVENTIONS.md).

## Reusable workflows

| Workflow | Does | Caller permissions |
|---|---|---|
| `service.yml` | Full service pipeline (below). Use this. | `contents: write`, `pull-requests: write`, `packages: write` |
| `pr-title.yml` | PR title is a Conventional Commit | `pull-requests: read` |
| `secrets-scan.yml` | gitleaks over the tree | `contents: read` |
| `container.yml` | Build multi-arch image; push `sha-<short>`; output digest | `contents: read`, `packages: write` |
| `release.yml` | release-please; optional major tag `vX` | `contents: write`, `pull-requests: write` |
| `promote.yml` | Release artifact: image digest tagged `X.Y.Z`, `X.Y`; chart at release commit with digest baked in, pushed to `oci://ghcr.io/alterworld-hub/charts/<name>:X.Y.Z` | `contents: read`, `packages: write` |
| `gitops-bump.yml` | PR in `gitops`: set `<app>` release on nodes; auto-merge | none (uses bot token) |

`service.yml`:
- PR: pr-title, secrets-scan, image build (no push).
- `main`: secrets-scan, image push `sha-<short>`, release-please.
- Release: promote the image of the release commit to `X.Y.Z`. Same digest as `sha-<short>`.
- Then: bot PR in `gitops` setting the chart version in `nodes/<node>/apps/<app>.version.yaml` for `deploy-nodes` (default `local`), auto-merged when checks pass. One value per node = atomic rollout (chart pins the image).

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

Org secret `BOT_PRIVATE_KEY` = private key of GitHub App `alterworld-hub-bot` (contents, pull-requests: write). release-please acts as the bot so release PRs trigger CI.

Required checks for `main`: `check`, `service / image / build`, `service / pr-title / check`, `service / secrets-scan / gitleaks`.

## Build speed rules
- No `RUN` under emulation. Arch-independent output (JS): build stage `FROM --platform=$BUILDPLATFORM`. Binaries (Rust): cross-compile or native arm64 runners. `qemu: true` only as last resort.
- `cache-mode: min` by default; `max` only when rebuilding layers costs more than exporting them (e.g. Rust deps).
