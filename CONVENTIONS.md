# Conventions

Org-wide rules for `alterworld-hub`. Terse by design: read by humans and agents.

## Text
- All text in git is English: code, comments, docs, commits, PRs.
- Agent-facing docs (`CONVENTIONS.md`, `AGENTS.md`, READMEs): facts and rules only, no prose.

## Repos
| Repo | Owns |
|---|---|
| `.github` | Reusable workflows, templates, conventions |
| `gitops` | Desired state of every node |
| `<service>` | Code, `Dockerfile`, Helm chart, CI caller |

## Commits and PRs
- [Conventional Commits 1.0](https://www.conventionalcommits.org/en/v1.0.0/).
- Types: `feat` `fix` `perf` `refactor` `docs` `test` `build` `ci` `chore` `revert`.
- Scope optional, kebab-case: `feat(search): add plate filter`.
- Breaking change: `!` after type/scope and a `BREAKING CHANGE:` footer.
- Squash merge only. PR title becomes the commit, so PR title must be a valid Conventional Commit (checked by CI).
- Trunk-based. `main` is always releasable. Branch names: `<type>/<short-desc>`.

## Versioning
- [SemVer 2.0](https://semver.org/). Tags `vX.Y.Z`.
- Versions come from commits via release-please. Never bump by hand.
- `0.x` = unstable API.
- Repos consumed by ref (`.github`) also move a major tag `vX`.

## Images
- Registry: `ghcr.io/alterworld-hub/<repo>`.
- Tags: `sha-<short>` from `main`, `X.Y.Z` and `X.Y` from releases. Never `latest`.
- Deploy by digest (`@sha256:…`), never by tag.
- Multi-arch: `linux/amd64`, `linux/arm64`.

## Naming
| Thing | Style | Example |
|---|---|---|
| Repo, service, image, Helm release | kebab-case | `event-gateway` |
| Event type | `<entity>.<past-verb>` | `vehicle.detected` |
| Postgres db/role | snake_case | `event_gateway` |
| RabbitMQ user/exchange/queue | kebab-case + dots | `event-gateway.events` |
| Env var | UPPER_SNAKE, `<SERVICE>_<RESOURCE>_<KEY>` | `EVENT_GATEWAY_POSTGRESQL_PASSWORD` |
| Node path | `/`-separated DNS labels | `root/org-a/site-1` |

## GitHub Actions
- Shared logic lives in `.github/workflows/*.yml` of this repo (`on: workflow_call`).
- Callers pin a major tag: `alterworld-hub/.github/.github/workflows/<file>@v0`.
- First-party actions (`actions/*`, `docker/*`, `googleapis/*`): pinned by major tag.
- Third-party actions: pinned by full commit SHA with a version comment.
- Least-privilege `permissions:` on every workflow.

## Secrets
- Never in plaintext in git. Encrypted with SOPS where needed.
- Every repo runs the secrets scan in CI.
