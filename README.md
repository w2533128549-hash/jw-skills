# JW Skills

Reusable Codex skills for personal use.

## Skills

- `create-multi-agent-project`: Codex skill that scaffolds a project-local multi-agent team with a project manager and specialist agents, an `agents/` directory, `config.toml`, and `AGENTS.md`. Enforces workspace-only writes and high-risk handoff to the project manager.

## Install into Codex

Codex loads skills from `$CODEX_HOME/skills` (defaults to `~/.codex/skills` on macOS/Linux and `%USERPROFILE%\.codex\skills` on Windows). After installing, restart Codex so it picks up the new skill.

### Option 1: use the built-in `skill-installer` skill

In Codex, ask:

> Use the skill-installer skill to install `create-multi-agent-project` from `w2533128549-hash/jw-skills` at path `skills/create-multi-agent-project`.

Codex will call `scripts/install-skill-from-github.py --repo w2533128549-hash/jw-skills --path skills/create-multi-agent-project`.

### Option 2: install via git (recommended for offline reuse)

Windows PowerShell:

```powershell
$dest = "$env:USERPROFILE\.codex\skills\create-multi-agent-project"
if (Test-Path -LiteralPath $dest) { Remove-Item -LiteralPath $dest -Recurse -Force }
$tmp = New-TemporaryFile
Remove-Item $tmp
$repo = "$env:TEMP\jw-skills-$([System.Guid]::NewGuid())"
git clone --depth 1 https://github.com/w2533128549-hash/jw-skills.git $repo
Copy-Item -Recurse -Force "$repo\skills\create-multi-agent-project" $dest
Remove-Item -Recurse -Force $repo
```

macOS/Linux:

```bash
dest="${CODEX_HOME:-$HOME/.codex}/skills/create-multi-agent-project"
rm -rf "$dest"
tmp=$(mktemp -d)
git clone --depth 1 https://github.com/w2533128549-hash/jw-skills.git "$tmp"
cp -R "$tmp/skills/create-multi-agent-project" "$dest"
rm -rf "$tmp"
```

### Option 3: download the folder without git

Windows PowerShell (uses GitHub tarball, no git required):

```powershell
$dest = "$env:USERPROFILE\.codex\skills\create-multi-agent-project"
if (Test-Path -LiteralPath $dest) { Remove-Item -LiteralPath $dest -Recurse -Force }
$tmp = "$env:TEMP\jw-skills-$([System.Guid]::NewGuid())"
New-Item -ItemType Directory -Path $tmp | Out-Null
$tar = "$tmp\repo.tar.gz"
Invoke-WebRequest -Uri "https://codeload.github.com/w2533128549-hash/jw-skills/tar.gz/refs/heads/main" -OutFile $tar
tar -xzf $tar -C $tmp
$src = Get-ChildItem -Directory $tmp | Where-Object { $_.Name -like 'jw-skills-*' } | Select-Object -First 1
Copy-Item -Recurse -Force "$($src.FullName)\skills\create-multi-agent-project" $dest
Remove-Item -Recurse -Force $tmp
```

After any of the above, restart Codex so the new skill is loaded.

## Usage

Once installed, ask Codex:

> Use `create-multi-agent-project` to scaffold this project.

The skill will create `agents/`, `config.toml`, and `AGENTS.md` in the current project root and route high-risk work through the project manager agent.
