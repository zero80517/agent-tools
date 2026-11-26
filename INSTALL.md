# Install

These steps are shared by all harnesses. Where a step depends on the harness, follow the linked file:

- **Claude Code:** [.claude/INSTALL.md](.claude/INSTALL.md)
- **OpenCode:** [.opencode/INSTALL.md](.opencode/INSTALL.md)

Do the steps once for each harness you use. You need Git.

> [!NOTE]
> **Agents:** install for the harness you're running in, unless the user asks otherwise. Do step 1 first. The linked files are then available in the cloned project, relative to its root.

## 1. Get this project

```bash
git clone https://github.com/zero80517/agent-tools.git
cd agent-tools
```

If you already have it, run `git pull` instead.

## 2. Copy the stored skills

This copies every folder in `skills/` into the harness's global skills folder.

> [!WARNING]
> A skill folder with the same name is **deleted and replaced**, including any edits you made there. Edit DIY skills in this project, then copy them again.

Other skills in the global folder aren't touched. This also means that a skill you delete or rename here stays installed until you remove it yourself.

Get the destination from your harness file: [Claude Code](.claude/INSTALL.md#skills-folder) · [OpenCode](.opencode/INSTALL.md#skills-folder). Set it in the first line, then run the commands from the project root.

**PowerShell**

```powershell
$dest = "<skills folder>"

$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force $dest | Out-Null
Get-ChildItem skills -Directory | ForEach-Object {
    $target = Join-Path $dest $_.Name
    if (Test-Path $target) { Remove-Item $target -Recurse -Force }
    Copy-Item $_.FullName $target -Recurse
}
```

**Bash**

```bash
dest="<skills folder>"

mkdir -p "$dest"
for src in skills/*/; do
    name=$(basename "$src")
    rm -rf "${dest:?}/$name" && cp -R "skills/$name" "$dest/$name"
done
```

## 3. Install superpowers

The steps depend on the harness: [Claude Code](.claude/INSTALL.md#superpowers) · [OpenCode](.opencode/INSTALL.md#superpowers)

## 4. Install the agents (OpenCode only)

See [OpenCode](.opencode/INSTALL.md#agents).

## Finish

Restart the harness so it loads the changes.

To update later, repeat steps 1, 2 and 4. External projects update as described in your harness file.
