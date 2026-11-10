# perplexity-answer-engine

Answers a factual or current question the way Perplexity does: it searches the live web, opens the strongest pages, and gives a short answer where every claim points to a numbered source with its date. It never answers from memory. Use it when you want a quick, checkable answer with sources, not a long report.

## When to use it
- You ask "what is the latest on X", "is it true that Y", or "X vs Y" and need sources you can click.
- You want to know what is not verified, not only what is found.
- You want follow-up questions that go deeper into the topic.

## Example request
> /perplexity-answer-engine does the EU AI Act's general-purpose AI rules start on 2 August 2025?

## Example output

**Answer**
The obligations for general-purpose AI (GPAI) model providers under the EU AI Act applied from 2 August 2025 [1][2]. The Commission's fact page says the obligations "enter into application" on that date [1], and Baker McKenzie says they cover models placed on the market on or after it [2].

**Details**
- The Commission's fact page was last updated on 1 August 2025 [1].
- The Baker McKenzie article is dated 6 August 2025 [2].

**Not verified**
- Transition period for models already on the market: search snippets from Mayer Brown and Orrick say models placed on the market before 2 August 2025 have until 2 August 2027. Neither page was opened, and the two pages that were opened say nothing about a transition period.
- Commission fines from 2 August 2026: found only in a search snippet and not checked.

**Sources**
[1] General-purpose AI obligations under the AI Act - European Commission Digital Strategy - last updated 1 August 2025 - https://digital-strategy.ec.europa.eu/en/factpages/general-purpose-ai-obligations-under-ai-act
[2] General-purpose AI Obligations Under the EU AI Act Kick in From 2 August 2025 - Baker McKenzie - 6 August 2025 - https://bakermckenzie.com/en/insight/publications/2025/08/general-purpose-ai-obligations

**Related**
1. Which models count as having systemic risk under the GPAI rules?
2. What must a GPAI provider publish about its training data?
3. Does the AI Act text itself give a transition period of until 2 August 2027 for older models?

What this run shows: the start date has two independent sources, one of them the European Commission. The older-model deadline is marked "Not verified" because it appeared only in search snippets, which the skill does not accept as proof.

## Install
```bash
cp -r perplexity-answer-engine ~/.claude/skills/
```
Full instructions for the agent: [SKILL.md](SKILL.md)

Last run: 2026-11-10 · Claude Haiku 5.5
