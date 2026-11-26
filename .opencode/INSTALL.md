# OpenCode specifics

Start with [INSTALL.md](../INSTALL.md). This file only covers what's different in OpenCode.

## Skills folder

Use `$HOME/.config/opencode/skills` as the destination. It works in both PowerShell and Bash.

## superpowers

Add the plugin to your global OpenCode config, `~/.config/opencode/opencode.json` or `opencode.jsonc`. Keep your existing settings.

For OpenCode 2.0.4 or later:

```json
{
  "plugins": ["superpowers@git+https://github.com/obra/superpowers.git"]
}
```

OpenCode V1 uses the key `plugin` instead of `plugins`.

For updates and Windows installation problems, see the [original instructions](https://github.com/obra/superpowers/blob/main/.opencode/INSTALL.md).

## Agents

This copies the files in `agents/` into OpenCode's global agents folder. Files with the same name are **overwritten**. Run from the project root.

**PowerShell**

```powershell
New-Item -ItemType Directory -Force "$HOME/.config/opencode/agents" | Out-Null
Copy-Item agents/*.md "$HOME/.config/opencode/agents" -Force
```

**Bash**

```bash
mkdir -p "$HOME/.config/opencode/agents"
cp agents/*.md "$HOME/.config/opencode/agents/"
```

`flash-worker` uses a `routerai` model, so set up the `routerai` provider in your OpenCode config first, or change the `model` line in [agents/flash-worker.md](../agents/flash-worker.md) before copying. Check that your provider offers that model.
