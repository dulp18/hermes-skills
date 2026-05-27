# Sharing Hermes Skills via GitHub

This is the canonical workflow for backing up and sharing Hermes skills through a GitHub repository. Others can subscribe to your skills via `hermes skills tap add https://github.com/<user>/hermes-skills`.

## Why GitHub Over Notion

- Skills are Markdown files — Git is the natural version-control system
- Hermes natively supports `hermes skills tap add REPO` for GitHub repos
- Free, no extra accounts needed, public or private
- PR workflow for collaboration

## Setup (One-Time)

### 1. GitHub Authentication

```bash
# Generate SSH key (ed25519)
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519 -N ""

# Copy to clipboard on macOS (avoids paste errors)
cat ~/.ssh/id_ed25519.pub | pbcopy

# Add key at: https://github.com/settings/keys → "New SSH key" → Authentication Key

# Configure git to use SSH for GitHub
git config --global url."git@github.com:".insteadOf "https://github.com/"

# Test
ssh -T git@github.com
# Expected: "Hi <username>! You've successfully authenticated..."

# gh CLI
brew install gh                                # macOS
gh auth login --git-protocol ssh --hostname github.com --web
# If web flow times out, use the device code it prints
```

### 2. Git Identity

```bash
git config --global user.name "your-github-username"
git config --global user.email "your-email@example.com"
```

## Create the Skills Repo

```bash
# Create repo on GitHub
gh repo create hermes-skills --public --description "My Hermes Agent skills collection" --clone
cd hermes-skills

# Set up directory structure
mkdir -p scripts references
```

## Sync Skills: Local → Repo

```bash
#!/bin/bash
# scripts/export-skills.sh — copies local skills into the repo
SKILLS_SRC="$HOME/.hermes/skills"
SKILLS_DST="."  # repo root

# For user-created skills only (skip builtins):
for skill_dir in "$SKILLS_SRC"/*/; do
  name=$(basename "$skill_dir")
  # Skip builtin categories if desired
  if [ -f "$skill_dir/SKILL.md" ]; then
    mkdir -p "$SKILLS_DST/$name"
    cp -r "$skill_dir"/* "$SKILLS_DST/$name/"
  fi
done

echo "Skills exported. Review and commit:"
echo "  git add . && git commit -m 'Update skills' && git push"
```

## Sync Skills: Repo → Local (Subscribe)

Anyone can subscribe to your skills repo:

```bash
hermes skills tap add https://github.com/<username>/hermes-skills
hermes skills install <skill-name>
```

## Directory Convention

```
hermes-skills/
├── README.md              # What's in here, how to subscribe
├── scripts/
│   └── export-skills.sh   # Sync local → repo
├── <category>/            # e.g. productivity/, creative/, mlops/
│   └── <skill-name>/
│       └── SKILL.md
│       └── references/    # (optional)
│       └── scripts/       # (optional)
└── .gitignore
```
