# Changelog

This project uses [Semantic Versioning](https://semver.org/). The current version is also in [VERSION](VERSION).

## 0.2.0 - 2026-11-26

### Added

- OpenCode installation asks which models `worker` and the built-in `explore` agent use, and saves them in the OpenCode config.

### Changed

- Renamed the `flash-worker` agent to `worker`. If the old file is still installed, the install steps ask before deleting it.
- `worker` no longer sets a model.
- `worker` reports changed files, commands, evidence and blockers, and says tests passed only if it ran them.
- `orchestrator` is in English and replies in the user's language. Its references to specific tools and standards are now generic.
- `orchestrator` requires a delegation list only when a request needs delegation or it delegated something.
- `orchestrator` says when to use `general`, and runs tasks that edit the same files one at a time.

### Fixed

- `orchestrator` now has permission rules that block reading files outside skill folders.

## 0.1.0 - 2026-11-26

### Added

- The `git-commit` skill, from `github/awesome-copilot`.
- The `grill-me` and `grill-with-docs` skills, from `mattpocock/skills`, with the skills they require.
- The `orchestrator` and `flash-worker` agents for OpenCode.
- Install instructions for Claude Code and OpenCode, including superpowers.
- `sources.json` and `scripts/fetch.py` to update stored third-party skills.
- README, glossary and third-party notices.
