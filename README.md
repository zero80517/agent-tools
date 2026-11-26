# 🧰 Agent Tools

The skills, agents and scripts I've made or found, kept in one place and shared across harnesses and PCs.

**Quick install:** tell your agent (Claude Code or OpenCode):

```
Fetch and follow instructions from https://raw.githubusercontent.com/zero80517/agent-tools/refs/heads/main/INSTALL.md
```

**Version:** see [VERSION](VERSION) · **Changes:** [CHANGELOG.md](CHANGELOG.md) · **Setup:** [INSTALL.md](INSTALL.md)

## ✨ Skills

| Skill | Usage | Description | Source |
|---|---|---|---|
| `git-commit` | `commit` | Examines the diff, stages related files and makes a Conventional Commits commit. | [awesome-copilot](https://github.com/github/awesome-copilot/blob/main/skills/git-commit/SKILL.md) |
| `writing-skills` | `write-skill` | Guides you through creating, editing and testing skills. | [superpowers](https://github.com/obra/superpowers) (external) |
| `grill-me` | `plan` | Interviews you relentlessly to sharpen a plan or design. | [mattpocock/skills](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) |
| `grill-with-docs` | `plan`, `docs` | The same interview, writing ADRs and a glossary as you go. | [mattpocock/skills](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md) |

**External** skills aren't stored here. They come with their whole project, which you [install separately](INSTALL.md). [superpowers](https://github.com/obra/superpowers/tree/main/skills) includes many more skills than the one listed above.

## 🤖 Agents

These work in **OpenCode only**.

| Agent | Usage | Description | Source |
|---|---|---|---|
| [`orchestrator`](agents/orchestrator.md), [`flash-worker`](agents/flash-worker.md) | `plan`, `subagents` | `orchestrator` plans, delegates all execution and reviews the reports. `flash-worker` is one of its subagents, for coding, file edits and tests. | DIY |

## 📜 Scripts

[`scripts/fetch.py`](scripts/fetch.py) checks the stored third-party skills against their sources. It needs Python 3.9 or later and Git.

```bash
python scripts/fetch.py          # report what changed upstream
python scripts/fetch.py --apply  # update the stored copies
```

After `--apply`, review `git diff`, update `VERSION` and `CHANGELOG.md`, and commit. The script doesn't install or commit anything. Check whether an updated skill now needs another skill, because the script won't detect that.

## 🗂️ Layout

| Path | Contents |
|---|---|
| `skills/` | Skills stored here, one folder each |
| `agents/` | Agent definitions |
| `scripts/` | Maintenance scripts |
| [`sources.json`](sources.json) | Where stored third-party skills come from, and the external projects |
| [`GLOSSARY.md`](GLOSSARY.md) | The terms this project uses |

## ➕ Adding things

- **DIY skill:** add `skills/<name>/SKILL.md`, then add a row above with `DIY` as the source.
- **Third-party skill:** add an entry under `skills` in `sources.json`, with `commit` set to `""`. Run `python scripts/fetch.py --apply`, then add a table row and the license to [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Don't edit the stored copy, because the next update overwrites it.
- **External project:** add it under `external` in `sources.json`, add its install steps to [INSTALL.md](INSTALL.md) and the harness files, and add table rows for the skills you care about.

Reuse an existing **Usage** label before creating a new one.

## ⚖️ Licensing

Third-party skills keep their authors' licenses. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The DIY work doesn't have a license yet.
