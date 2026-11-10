# perplexity-answer-engine

Answers a factual or current question the way Perplexity does: it searches the live web, opens the strongest pages, and gives a short answer where every claim points to a numbered source with its date. It never answers from memory. Use it when you want a quick, checkable answer with sources, not a long report.

## When to use it
- You ask "what is the latest on X", "is it true that Y", or "X vs Y" and need sources you can click.
- You want to know what is not verified, not only what is found.
- You want follow-up questions that go deeper into the topic.

## Example request
> /perplexity-answer-engine pro what are the latest 5 released AI models from Anthropic?

## Example output

**Answer**
The 5 newest Anthropic models are Claude Fable 5.2 and Claude Mythos 5.2 (both Nov 9, 2026), Claude Haiku 5.5 (Oct 7), Claude Sonnet 5.5 (Sep 28) and Claude Opus 5.5 (Sep 22) [1][2]. Fable 5.2 and Mythos 5.2 are the same underlying model with different safeguards. Fable 5.2 is open to all paid users, while Mythos 5.2 is limited to vetted organizations [2][3][4].

**Details**

| # | Model | Released | API ID | Short note |
|---|---|---|---|---|
| 1 | Claude Fable 5.2 | Nov 9, 2026 | claude-fable-5-2 | Top model for hard coding and science work. Up to 30% faster than Fable 5.1 [2][3][5]. |
| 2 | Claude Mythos 5.2 | Nov 9, 2026 | not listed in docs | Safeguards are lifted in some areas. Access is through the Life Sciences and Cyber Verification Programs [3][4]. |
| 3 | Claude Haiku 5.5 | Oct 7, 2026 | claude-haiku-5-5 | Fastest small model for high-volume tasks [1][5]. |
| 4 | Claude Sonnet 5.5 | Sep 28, 2026 | claude-sonnet-5-5 | Over 30% faster than Sonnet 5, up to 30% cheaper per task [1][5]. |
| 5 | Claude Opus 5.5 | Sep 22, 2026 | claude-opus-5-5 | Strong in agentic coding (AI that works on tasks by itself). Anthropic recommends it as the starting model for most work [1][4][5]. |

Price per million tokens (input / output): Fable 5.2 is $8 / $40, Opus 5.5 is $4 / $20, Sonnet 5.5 is $2 / $10 [5].
All four models in the docs table have a 1M-token context window and 128K max output [5].
If you count only models open to the public, the fifth spot goes to Fable 5.1 (Sep 1, 2026) [6].

**Not verified**
- Mythos 5.2 does not appear in the API docs table, so its API ID and public availability could not be confirmed [5].
- The Fable 5.1 date (Sep 1) comes from Wikipedia only. No Anthropic page for it was opened [6].
- The docs page shows no release dates. Dates come from Anthropic's news list and press coverage [1][3].

**Sources**
[1] Anthropic News (release list) - anthropic.com - entries dated Sep 22 to Nov 9, 2026 - https://www.anthropic.com/news
[2] Introducing Claude Fable 5.2 and Claude Mythos 5.2 - anthropic.com - Nov 9, 2026 - https://www.anthropic.com/claude-fable-and-mythos-5-2
[3] Anthropic releases Claude Fable 5.2 and Claude Mythos 5.2 ahead of IPO - CNBC - Nov 9, 2026 - https://www.cnbc.com/2026/11/09/anthropic-claude-fable-5-2-mythos-5-2.html
[4] Anthropic Launches Claude Fable 5.2 and Mythos 5.2 - MacRumors - Nov 9, 2026 - https://www.macrumors.com/2026/11/09/anthropic-launches-claude-fable-5-2/
[5] Models overview - platform.claude.com - no date - https://platform.claude.com/docs/en/models/overview
[6] Claude Mythos - Wikipedia - no date - https://en.wikipedia.org/wiki/Claude_Mythos

**Related**
1. How do Fable 5.2 and Opus 5.5 compare on price per task and benchmarks?
2. What changed between Fable 5.1 and Fable 5.2 (blocks, speed, token use)?
3. Which Claude 5.5 model fits which kind of agent work?

What this example shows: pro mode gives a dated table, sources numbered in order of first use, and a "Not verified" section that names each gap. This example was pasted in from a prior answer. It was not a live run.

## Install
```bash
cp -r perplexity-answer-engine ~/.claude/skills/
```
Full instructions for the agent: [SKILL.md](SKILL.md)

Example source: pasted answer, not a live run · added 2026-11-10 · Claude Haiku 5.5
