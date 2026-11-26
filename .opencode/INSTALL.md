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

### Old agents

`flash-worker` is now called `worker`. Copying doesn't remove the old file. If `~/.config/opencode/agents/flash-worker.md` exists, ask the user whether to delete it. Delete it only if they agree.

Then [choose the models](#models).

## Models

The agent files don't set a model. You choose one for `worker` and one for the built-in `explore` agent in your global OpenCode config.

> [!IMPORTANT]
> **Agents:** ask the user which models to use. Don't choose for them.

1. Run `opencode models` to list the models available on this PC.
2. Read the global config, `~/.config/opencode/opencode.json` or `opencode.jsonc`, and note the current model of each of the two agents, if any.
3. Ask two separate questions: which model for `worker`, and which for `explore`. In each one:
   - If the agent already has a model, offer to keep it, as the first option.
   - If it has none, offer to skip. A skipped agent gets no model setting, so it uses the model of the session that calls it.
   - Offer the models from step 1, and let the user type another model ID. If that ID isn't in the list, warn them and ask them to confirm it.
4. Add each chosen model to the config. Edit the existing file, keeping its other settings and comments. If there's no config file, create `opencode.json`.

Use the `agent` key. If the file already has an `agents` key, add the models there instead. Replace `<provider/model>` with the chosen IDs:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "worker": {
      "model": "<provider/model>"
    },
    "explore": {
      "model": "<provider/model>"
    }
  }
}
```

A model's provider must be set up in your OpenCode config or signed in to.
