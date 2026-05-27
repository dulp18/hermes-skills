#!/usr/bin/env python3
"""Sync Hermes skills between local (~/.hermes/skills/) and this repo."""

import os
import sys
import shutil
from pathlib import Path

HERMES_SKILLS = Path.home() / ".hermes" / "skills"
REPO_ROOT = Path(__file__).resolve().parent.parent


def export_skills():
    """Copy skills from ~/.hermes/skills/ → repo (overwrite)."""
    if not HERMES_SKILLS.exists():
        print(f"❌ {HERMES_SKILLS} not found")
        sys.exit(1)

    count = 0
    for skill_md in HERMES_SKILLS.rglob("SKILL.md"):
        rel = skill_md.relative_to(HERMES_SKILLS)
        dest = REPO_ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_md, dest)
        count += 1

    # Remove stale skill dirs that no longer exist locally
    for repo_skill in REPO_ROOT.rglob("SKILL.md"):
        rel = repo_skill.relative_to(REPO_ROOT)
        # Skip scripts/, .git/, etc.
        if rel.parts[0] in ("scripts", ".git", "__pycache__"):
            continue
        if not (HERMES_SKILLS / rel).exists():
            # Remove the entire skill directory
            shutil.rmtree(repo_skill.parent)
            print(f"  🗑  removed stale: {rel.parent}")

    print(f"✅ Exported {count} skills to {REPO_ROOT}")


def import_skills():
    """Copy skills from repo → ~/.hermes/skills/ (overwrite)."""
    count = 0
    for repo_skill in REPO_ROOT.rglob("SKILL.md"):
        rel = repo_skill.relative_to(REPO_ROOT)
        if rel.parts[0] in ("scripts", ".git", "__pycache__"):
            continue
        dest = HERMES_SKILLS / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repo_skill, dest)
        count += 1

    print(f"✅ Imported {count} skills to {HERMES_SKILLS}")


def diff_skills():
    """Show skills that differ between local and repo."""
    local = set()
    if HERMES_SKILLS.exists():
        for md in HERMES_SKILLS.rglob("SKILL.md"):
            local.add(str(md.relative_to(HERMES_SKILLS)))

    repo = set()
    for md in REPO_ROOT.rglob("SKILL.md"):
        rel = str(md.relative_to(REPO_ROOT))
        if not rel.startswith(("scripts/", ".git/", "__pycache__/")):
            repo.add(rel)

    only_local = local - repo
    only_repo = repo - local

    if only_local:
        print(f"📁 Only in local ({len(only_local)}):")
        for p in sorted(only_local):
            print(f"   + {p}")
    if only_repo:
        print(f"📁 Only in repo ({len(only_repo)}):")
        for p in sorted(only_repo):
            print(f"   + {p}")
    if not only_local and not only_repo:
        print("✅ Local and repo are in sync")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("export", "import", "diff"):
        print("Usage: sync.py <export|import|diff>")
        print()
        print("  export   Copy local skills → repo    (before git commit)")
        print("  import   Copy repo skills → local    (after git pull)")
        print("  diff     Show what's different")
        sys.exit(1)

    action = sys.argv[1]
    if action == "export":
        export_skills()
    elif action == "import":
        import_skills()
    elif action == "diff":
        diff_skills()


if __name__ == "__main__":
    main()
