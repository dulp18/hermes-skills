---
name: skills-github-sync
description: "Sync Hermes skills between local (~/.hermes/skills/) and GitHub repo — export, import, diff, and auto-commit."
version: 1.0.0
---

# Skills GitHub Sync

Sync Hermes Agent skills between the local `~/.hermes/skills/` directory and the GitHub repo at `~/hermes-skills/` (https://github.com/dulp18/hermes-skills).

## Trigger

Use this skill when the user asks to:
- "sync skills to GitHub" / "push skills"
- "backup skills" / "export skills"
- "pull skills" / "import skills"
- "update the skills repo"

## Prerequisites

- GitHub SSH key at `~/.ssh/id_ed25519` (already configured)
- `gh` CLI installed and authenticated
- Git configured: `user.name=dulp18`, `user.email=linpeng_du@163.com`
- PAT saved in `~/.hermes/.env` as `GITHUB_TOKEN`

## Usage

### Export: push local skills to GitHub

```bash
cd ~/hermes-skills
python3 scripts/sync.py export
git add -A
git commit -m "sync: export skills $(date +%Y-%m-%d)"
git push
```

If no changes: skip commit and say "no changes to sync".

### Import: pull GitHub skills to local

```bash
cd ~/hermes-skills
git pull
python3 scripts/sync.py import
```

### Diff: show what's different

```bash
cd ~/hermes-skills
python3 scripts/sync.py diff
```

### When a new skill is created in Hermes

After `skill_manage(action='create', ...)` succeeds:
1. Run export (the sync script copies the new SKILL.md into the repo)
2. Commit and push

## Sync script

Located at `~/hermes-skills/scripts/sync.py`. It:
- **export**: copies all `SKILL.md` files from `~/.hermes/skills/` → `~/hermes-skills/`, preserving directory structure. Removes stale skill dirs from repo that no longer exist locally.
- **import**: copies from `~/hermes-skills/` → `~/.hermes/skills/`
- **diff**: lists skills that exist only in local or only in repo

## Pitfalls

- Always run `export` BEFORE `git commit` — the sync script updates files in the repo working tree
- After `git pull` from the repo, run `import` to get new skills into ~/.hermes/skills/
- The sync script only copies `SKILL.md` files — supporting files (references/, templates/, scripts/) in skill directories are NOT synced. If a skill has supporting files (.py scripts, .tex templates, .json configs, .html references, etc.), copy them manually.
- The repo is at `~/hermes-skills/`, NOT inside `~/.hermes/` — don't accidentally clone into the hermes config directory
