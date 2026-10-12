# tweet-post

Writes a 100–120 word X/Twitter post about technical work, in plain A2–B1 English. It suits developers and researchers who want to announce a project, paper, or finding. Every post follows the same arc: hook, turn, substance, reasoning, close, plus 2–3 specific hashtags.

## When to use it
- You built a skill, tool, or project and want to announce it on X.
- You want to share someone else's paper or finding without inventing or rounding its numbers.
- You have a README, SKILL.md, or abstract and want a tweet from it, in English or Arabic (fusha).

## Example request
> Write a tweet announcing my AISkills repo: https://github.com/IbrahimSobh/AISkills

## Example output
> Good prompts get lost. They live in old chats, and the next task starts from zero.
>
> To fix this, here's AISkills: an open-source collection of AI skills under the MIT license. Each skill is one folder with a SKILL.md file. It tells an AI agent when to use the skill and how.
>
> ✅ fact-checker rates claims against cited sources
> 📰 ai-news-weekly writes a fact-only 7-day briefing
> 🐦 tweet-post writes tweets in a fixed structure
> 🩺 skill-doctor reviews other skills
>
> There are 7 skills in total. I keep each skill in its own folder on purpose, because a folder you can copy is a skill you can reuse.
>
> Skills in folders last. Prompts in chats disappear.
>
> #AIAgents #ClaudeCode #OpenSource
>
> https://github.com/IbrahimSobh/AISkills

(111 words + 3 hashtags)

_Last run: 2026-10-12 · Claude Sonnet 5.5_

## Install
```bash
cp -r tweet-post ~/.claude/skills/
```
Full instructions for the agent: [SKILL.md](SKILL.md)
