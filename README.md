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
| `promote.yml` | Tag a built digest as `X.Y.Z`, `X.Y` (no rebuild) | `packages: write` |

`service.yml`:
- PR: pr-title, secrets-scan, image build (no push).
- `main`: secrets-scan, image push `sha-<short>`, release-please.
- Release: promote the image of the release commit to `X.Y.Z`. Same digest as `sha-<short>`.

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
```

Required checks for `main`: `check`, `service / image / build`, `service / pr-title / check`, `service / secrets-scan / gitleaks`.

## Build speed rules
- No `RUN` under emulation. Arch-independent output (JS): build stage `FROM --platform=$BUILDPLATFORM`. Binaries (Rust): cross-compile or native arm64 runners. `qemu: true` only as last resort.
- `cache-mode: min` by default; `max` only when rebuilding layers costs more than exporting them (e.g. Rust deps).
