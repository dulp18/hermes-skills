---
name: ai-news-digest
description: Daily AI news digest for social media — collect from arXiv, HN, tech media, format as casual Chinese morning brief, deliver via Telegram cron.
---

Generate daily AI news digests optimized for social media (Xiaohongshu, Telegram, etc.).

## Trigger
- User asks to set up daily/weekly AI news collection and delivery
- User wants AI news formatted for social media posting
- User says "帮我收集AI新闻" or similar

## User Preferences (CRITICAL)
- **Style**: Casual, approachable, like chatting with a friend. NOT academic or professional.
- **Length**: Brief — each item 1-2 sentences max. Total 6-8 items.
- **Per section**: 1-2 items only. Do NOT overwhelm with quantity.
- **Tone**: Plain language (大白话) to explain technical concepts. Occasional emoji and humor OK.
- **Language**: Chinese (中文)

## Workflow

### Step 1: Gather News
From three sources, pick 1-2 most interesting items each:

1. **arXiv** (cs.AI / cs.CL) — pick papers that are genuinely interesting, not just highly-cited
2. **Hacker News** — AI-related top posts
3. **Tech media** (TechCrunch, VentureBeat, The Verge) — major announcements

### Step 2: Format Output
Use this exact format:

```
☀️ **AI 早报 | {date}**

🤖 **今天值得看**
[One sentence about the most notable thing today — new model, tool, paper, or industry news. Casual tone.]

📄 **新论文**
• [Paper name] — [Plain-language explanation of what it does and why it's interesting]

🛠️ **新工具**
• [Tool name] — [What it is and what it does, one sentence]

📡 **动态**
• [News] — [One-line key takeaway]

---
💬 今日小记：[Optional occasional personal comment]
```

### Step 3: Set Up Cron Job
Create a cron job with:
- `schedule`: "0 8 * * *" (8 AM daily, adjust for user timezone)
- `deliver`: user's messaging platform (typically "telegram")
- `enabled_toolsets`: ["web", "browser", "terminal"]
- `repeat`: "forever"

## Setting Up

### Check delivery method first
Before creating the cron job, verify the delivery platform works:
```bash
hermes gateway status          # Is gateway running?
grep -i "telegram\|connecterror" ~/.hermes/logs/gateway.log | tail -5   # Any delivery errors?
```

### Cron job
```bash
hermes cron create "0 8 * * *"   # 8 AM daily (adjust timezone)
```
- Prompt: use `references/cron-prompt.md`
- Deliver: verify platform first — if Telegram fails (httpx.ConnectError is common in China), switch to CLI-only or use Discord/Slack
- Toolsets: `["web", "browser"]`
- Timeout: suggest 600s (default) — if the job times out with "API error recovery", the model may be struggling with web scraping; reduce scope to 4-5 items max

### Telegram connectivity in China
Telegram API IPs (149.154.167.220 etc.) are blocked from mainland China. Symptoms:
- Gateway log: `httpx.ConnectError`, `polling reconnect failed`, `Fallback IP ... failed`
- Cron: `delivery error: Telegram send failed: httpx.ConnectError`

Workarounds:
- Set `HTTP_PROXY`/`HTTPS_PROXY` env vars before starting gateway
- Use Discord/Slack/Email delivery instead
- Run via CLI: skip delivery, run `hermes chat -q "generate AI news digest"` and view in terminal

## Pitfalls
- ❌ Academic/professional tone — user finds this cold and hard to read
- ❌ Too many items per section — 3-5 is too many, stick to 1-2
- ❌ Long explanations — each item must be one sentence
- ❌ Jargon without plain-language translation
- ❌ Assuming Telegram works from China — always check gateway connectivity first
- ✅ Casual, friendly, brief — like a morning text from a friend who follows AI
