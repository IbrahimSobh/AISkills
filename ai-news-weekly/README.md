# ai-news-weekly

Generates a strict, fact-only weekly AI news briefing for the trailing 7 days. It sweeps editorial index pages and official lab sources, verifies each item's date and primary source, and returns a fixed-format report. For anyone who wants a trustworthy weekly digest instead of recycled headlines.

## When to use it
- You want a "what happened in AI this week" roundup with a stated UTC reporting window.
- You need every item tied to a direct primary-source link and an original publication date.
- You want near-misses and blind spots listed explicitly rather than hidden.

## Example request
> Give me this week's AI news.

## Example output
_Example run for the week of 2026-10-06 → 2026-10-12 (shortened). This is a snapshot, not current news._

```
# 🤖 Top AI News (Last 7 Days)
Reporting Window: 2026-10-06 → 2026-10-12 (UTC)

---

📰 Mistral AI introduces Mistral Large 4
Category: Foundation models
Organizations: Mistral AI
Published: 2026-10-06
Summary: Mistral Large 4 is a 1 trillion-parameter, natively multimodal model with 52 billion active parameters, available through a public preview API, with open weights due by the end of the month.
Original Source: https://mistral.ai/news/mistral-large-4/

---

📰 Anthropic introduces Claude Haiku 5.5
Category: Foundation models
Organizations: Anthropic
Published: 2026-10-07
Summary: Anthropic describes Claude Haiku 5.5 as the cheapest, fastest, and most capable small model it has released, priced at $0.10 per million input tokens and $0.50 per million output tokens for prompts up to 100k tokens.
Original Source: https://www.anthropic.com/claude-haiku-5-5

---

📰 AWS introduces Strands Box, open source sandboxes for AI agents
Category: Open source
Organizations: Amazon Web Services
Published: 2026-10-07
Summary: Strands Box, released under the Apache 2.0 license in developer preview, combines operating-system isolation with Dogwood policies that govern what an agent is allowed to do.
Original Source: https://aws.amazon.com/blogs/opensource/introducing-strands-box-ai-agent-sandboxes-powered-by-dogwood/

---

📰 Google Cloud introduces the Gemini agent
Category: Agents
Organizations: Google Cloud
Published: 2026-10-08
Summary: At its Gemini at Work 2026 event, Google Cloud unveiled Gemini as a single prompt-based agent that handles a wide range of business tasks and delivers finished work inside the tools people already use.
Original Source: https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/gemini-at-work/

---

📰 NVIDIA commits $1 billion to advance US science over five years
Category: Funding
Organizations: NVIDIA
Published: 2026-10-08
Summary: NVIDIA announced $1 billion in commitments over five years supporting U.S. higher-education research institutions, quantum leadership, and cloud service providers serving U.S. government missions.
Original Source: https://nvidianews.nvidia.com/news/nvidia-commits-1-billion-to-advance-us-science-over-the-next-five-years

---

…

# Weekly Summary

| Metric | Count |
|--------|------:|
| Total news items | 5 |
| Model releases | 2 |
| Research papers | 0 |
| Open-source projects | 1 |
| Product announcements | 1 |
| Infrastructure updates | 0 |
| Business/Funding | 1 |
| Safety/Regulation | 0 |
```

The full output also includes the Sources Checked, Not Checked, and Dropped Candidates lists.

_Last run: 2026-10-12 · Claude Sonnet 5.5_

## Install
```bash
cp -r ai-news-weekly ~/.claude/skills/
```
Full instructions for the agent: [SKILL.md](SKILL.md)
