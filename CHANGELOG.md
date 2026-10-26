# Changelog

## [0.9.0](https://github.com/alterworld-hub/.github/compare/v0.8.0...v0.9.0) (2026-10-26)


### Features

* require an issue reference in PR body; document bot app permissions ([#46](https://github.com/alterworld-hub/.github/issues/46)) ([a863cdb](https://github.com/alterworld-hub/.github/commit/a863cdbf35b93aaf6ee8e401add5d35c1a97b6c9))

## [0.8.0](https://github.com/alterworld-hub/.github/compare/v0.7.0...v0.8.0) (2026-10-26)


### ⚠ BREAKING CHANGES

* promote.yml inputs image/digest -> source-sha.

### Performance Improvements

* release the main image instead of rebuilding the release commit ([#44](https://github.com/alterworld-hub/.github/issues/44)) ([d0d8931](https://github.com/alterworld-hub/.github/commit/d0d89316a5b0accda118ef4ae4337068d714affe)), closes [#25](https://github.com/alterworld-hub/.github/issues/25)

## [0.7.0](https://github.com/alterworld-hub/.github/compare/v0.6.0...v0.7.0) (2026-10-26)


### Features

* keep only issues on the org project board ([#29](https://github.com/alterworld-hub/.github/issues/29)) ([a95c975](https://github.com/alterworld-hub/.github/commit/a95c975baf8068a608ac732fbb46f7429c0945c9))
* self-hosted renovate for all org repos ([#38](https://github.com/alterworld-hub/.github/issues/38)) ([dfd0bed](https://github.com/alterworld-hub/.github/commit/dfd0bed4feb5d979e038dd972a9444916c76976b))


### Bug Fixes

* **renovate:** use bot user id in git author ([#40](https://github.com/alterworld-hub/.github/issues/40)) ([f84d068](https://github.com/alterworld-hub/.github/commit/f84d0683eb80a259f04c459be4023f39f3bd8838)), closes [#39](https://github.com/alterworld-hub/.github/issues/39)

## [0.6.0](https://github.com/alterworld-hub/.github/compare/v0.5.1...v0.6.0) (2026-10-26)


### Features

* org project automation and issue forms ([#26](https://github.com/alterworld-hub/.github/issues/26)) ([b6644d2](https://github.com/alterworld-hub/.github/commit/b6644d2d2b7231062fe18234e97c389a0d403ba7))
* project-sync handles status lifecycle ([#28](https://github.com/alterworld-hub/.github/issues/28)) ([bcce8d1](https://github.com/alterworld-hub/.github/commit/bcce8d15d7cd6537c0bf773c3fdabac34af2667d))

## [0.5.1](https://github.com/alterworld-hub/.github/compare/v0.5.0...v0.5.1) (2026-10-26)


### Bug Fixes

* annotate multi-arch image index ([#16](https://github.com/alterworld-hub/.github/issues/16)) ([7ea9829](https://github.com/alterworld-hub/.github/commit/7ea9829bc5e69b34bc9911f01f9344140b2c52aa))

## [0.5.0](https://github.com/alterworld-hub/.github/compare/v0.4.1...v0.5.0) (2026-10-26)


### ⚠ BREAKING CHANGES

* promote.yml requires input `ref`.

### Features

* publish release chart with pinned image digest ([#13](https://github.com/alterworld-hub/.github/issues/13)) ([9c7c20a](https://github.com/alterworld-hub/.github/commit/9c7c20ac7f00b58596a6d51f7f2a941f6aea4e07))

## [0.4.1](https://github.com/alterworld-hub/.github/compare/v0.4.0...v0.4.1) (2026-10-26)


### Bug Fixes

* retry github api calls in gitops-bump ([#11](https://github.com/alterworld-hub/.github/issues/11)) ([283784a](https://github.com/alterworld-hub/.github/commit/283784a0c8b3a7dfe452d472df4e1b2ff85c0c7b))

## [0.4.0](https://github.com/alterworld-hub/.github/compare/v0.3.0...v0.4.0) (2026-10-26)


### Features

* deploy releases to nodes via bot PR in gitops ([#9](https://github.com/alterworld-hub/.github/issues/9)) ([ac1e0c5](https://github.com/alterworld-hub/.github/commit/ac1e0c54c99d42b57e8c482eb0bcd17cb3230711))

## [0.3.0](https://github.com/alterworld-hub/.github/compare/v0.2.0...v0.3.0) (2026-10-26)


### ⚠ BREAKING CHANGES

* release.yml and service.yml require secret BOT_PRIVATE_KEY.

### Features

* open release PRs as the org bot app ([#7](https://github.com/alterworld-hub/.github/issues/7)) ([7bbbad5](https://github.com/alterworld-hub/.github/commit/7bbbad5dc04401bc2aaf2074a1dcb6106be758de))

## [0.2.0](https://github.com/alterworld-hub/.github/compare/v0.1.0...v0.2.0) (2026-10-26)


### ⚠ BREAKING CHANGES

* container.yml drops `version` input.

### Features

* add service pipeline, promote without rebuild, faster image builds ([#4](https://github.com/alterworld-hub/.github/issues/4)) ([cd05f81](https://github.com/alterworld-hub/.github/commit/cd05f81d620f3468f21672aabdc5152f59378455))

## 0.1.0 (2026-10-26)


### Features

* add reusable workflows and org conventions ([570253c](https://github.com/alterworld-hub/.github/commit/570253c59a59da8d2b2ebe77c32b0bc151e9be3c))
