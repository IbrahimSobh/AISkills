# AISkills

A collection of useful AI skills. Each skill lives in its own folder with a `SKILL.md` file that tells an AI agent (such as Claude) when to use the skill and how to carry it out.

## Skills

| # | Skill | Description |
|---|---|---|
| 1 | [fact-checker](fact-checker/SKILL.md) | Checks the factual claims in a piece of text against reputable sources. Returns a Markdown table rating each claim ✅ Correct, 🟡 Partially Correct, or ❌ Incorrect, with cited references, and offers a corrected version of the text. Answers in the same language as the claims. |
| 2 | [ai-news-weekly](ai-news-weekly/SKILL.md) | Produces a fact-only briefing of the most significant AI news from the last 7 days (models, research, open source, tools, infrastructure, funding, safety and regulation). Every item is checked live against official primary sources and dated inside the window. The briefing ends with summary counts, the sources checked, any blind spots, and the candidates that were dropped. |

## Usage

To use a skill with Claude Code, copy its folder into your skills directory:

```bash
cp -r fact-checker ~/.claude/skills/
```

Then ask Claude to "fact-check" some text, or invoke the skill directly with `/fact-checker` or `/ai-news-weekly`.
