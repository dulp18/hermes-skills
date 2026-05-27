# hermes-skills

My [Hermes Agent](https://github.com/NousResearch/hermes-agent) skills collection — reusable AI agent workflows.

## What's here

Each directory contains one or more skills. A skill is a `SKILL.md` file that tells Hermes how to handle a specific task — from coding workflows to creative tools to API integrations.

## How to use

### Subscribe in Hermes

```bash
hermes skills tap add https://github.com/dulp18/hermes-skills
```

Then install individual skills:

```bash
hermes skills install <skill-name>
```

### Sync from local to repo

```bash
python3 scripts/sync.py export   # push local skills → repo
python3 scripts/sync.py import   # pull repo skills → local
```

## Skill format

```markdown
---
name: my-skill
description: "What this skill does"
version: 1.0.0
---

# My Skill

Step-by-step workflow...
```

## Author

[dulp18](https://github.com/dulp18)
