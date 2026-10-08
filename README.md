# AISkills

A collection of useful AI skills. Each skill lives in its own folder with a `SKILL.md` file that tells an AI agent (such as Claude) when to use the skill and how to carry it out.

## Skills

| # | Skill | Description |
|---|---|---|
| 1 | [fact-checker](fact-checker/SKILL.md) | Checks the factual claims in a piece of text against reputable sources. Returns a Markdown table rating each claim ✅ Correct, 🟡 Partially Correct, or ❌ Incorrect, with cited references, and offers a corrected version of the text. Answers in the same language as the claims. |

## Usage

To use a skill with Claude Code, copy its folder into your skills directory:

```bash
cp -r fact-checker ~/.claude/skills/
```

Then ask Claude to "fact-check" some text, or invoke `/fact-checker` directly.
