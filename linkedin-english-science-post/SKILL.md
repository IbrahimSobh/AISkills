---
name: linkedin-english-science-post
description: Turn a scientific paper, technical article, report, blog post, abstract, or research notes into an English LinkedIn post, plus three candidate hooks. Use this whenever the user shares a paper, arXiv link, abstract, PDF, research summary, or technical write-up and asks to "write a LinkedIn post", "post about this paper", "summarize this for LinkedIn", or wants to communicate a research finding to a professional English-speaking audience. Trigger it even when the user just drops a paper or link and says "make a post" without naming LinkedIn, and also when they ask only for hooks. Do not use for non-scientific LinkedIn posts (career updates, anecdotes, product or project announcements), for X/Twitter posts (use tweet-post), or for Arabic posts (use linkedin-arabic-science-post).
---

# LinkedIn English Scientific Post Generator

Write an English LinkedIn post that makes a complex scientific result understandable to a broad professional audience **without losing accuracy**. The audience is technically literate but not necessarily specialists in the paper's subfield.

The default deliverable is two sections, in this order: **Hooks → Final LinkedIn Post**. If the user asks for a subset (only hooks), give just that. If the user also wants a tweet about the same work, that is a separate job for the `tweet-post` skill.

## Before writing

**Whose work is it?** Assume the work is by someone else (a lab, a company, a set of authors). If there are signs the user may be an author (they say "our paper", "my team", or their name appears in the author list), ask one short question before writing: "Are you one of the authors?" The answer changes the voice (see *Attribution*).

**When input is thin.** If the user gives only a title or a link with no content, fetch the source or ask for it before writing. Never generate a plausible-sounding summary of a paper you haven't read. That is the single worst outcome for this skill: a confident, well-formatted, wrong post.

## Non-negotiables

These are what separate a good post from a bad one. Everything else is style.

**Never invent findings.** If the source is only a title and an abstract, work only from the title and abstract. You may infer the *structure* of the post, never the science. If something important is missing, say so and ask for it rather than filling the gap plausibly.

**Preserve numbers exactly.** If the paper reports a 12.4% improvement on a benchmark, the post says 12.4% on that benchmark. Never round it into a vibe ("a big improvement"). Never generalize a result on one dataset into a claim about all tasks.

**Do not upgrade correlation into causation**, and do not upgrade "on this benchmark, under these conditions" into "in general". If the authors hedge, the post hedges.

**Report limitations when they change the interpretation.** A result that only holds at 70B+ scale, was evaluated only in English, or used a weak baseline: that caveat belongs in the post. Not as a disclaimer dump; one honest sentence.

**Attribution.** When the work is by others, the post attributes it to them in the third person: "the Anthropic team", "researchers at DeepMind", "the paper's authors". Never let the summary drift into first person as if the user did this work. The only first-person voice is the *Reflection* section, which is the user's own commentary *on* the work. If the user confirmed they are an author, the body may use "we" and "our".

**Name only what the source states.** If the source doesn't state the authors' lab or affiliation, don't guess it from memory. Name the first author instead ("a study led by Jane Doe") or say "the authors".

**Date the work honestly.** Never call a work "new" or "recent" by default. If it isn't from the last few months, say the year ("a 2024 study").

## Language rules

Keep names of people, organizations, products, models, datasets, benchmarks, programming languages, frameworks, papers, conferences, standards, and technical terms exactly as the source writes them (GPT-4, MMLU, RLHF, Anthropic). Explain a term in plain words the first time it matters; don't replace it.

Short paragraphs: two to four lines each. LinkedIn's rendering punishes walls of text.

## Language level (A2–B1)

Write the post at **CEFR A2–B1 English**. This constrains sentence construction, not the ideas. Keep the thinking hard and the sentences easy.

- Sentences mostly under 20 words. One idea per sentence.
- Active voice. Subject-verb-object order.
- Common everyday verbs: "use" not "utilize", "start" not "commence", "show" not "demonstrate", "so" not "thereby".
- Simple connectors only: and, but, so, because, when, if, however, which means, for example. Avoid "whereby", "insofar as", "notwithstanding", "albeit".
- No idioms, no decorative metaphor, no phrasal verbs where a plain verb exists.
- Don't stack subordinate clauses. Split into two sentences instead.

**Exempt from the level cap.** These are not "advanced English" and must not be simplified away:

- Technical terms, jargon, and proper nouns.
- Code, commands, file paths, API and model names.
- Exact numbers, units, dataset and benchmark names.
- Verbatim quoted text from a source.

**Precision outranks the level.** If a simpler sentence would change the meaning, weaken a hedge, or drop a caveat, keep the harder construction. Never trade accuracy for reading level.

## Structure

### Section 1: Hooks

Produce exactly 3 hooks, roughly 13 words each. Each should provoke curiosity or challenge an assumption the reader likely holds. They should be genuinely different in angle, not three paraphrases of one idea.

LinkedIn shows only the first two lines before "…see more", so a hook must work on its own.

Useful patterns (not a checklist; reach for an original hook when you have one): "Do you think…", "Most people assume…", "Before you use…", "The hidden side of…", "What if…", "The real reason…"

No clickbait. The hook must be a claim the paper can actually support.

### Section 2: Final LinkedIn Post

200 to 300 words. Uses the strongest of the three hooks as its opening line.

**Body** covers, in accessible language:
1. What problem does the work address? (why anyone should care)
2. What did the researchers actually do? (the method, in one honest paragraph)
3. What did they find? (the result, with real numbers)
4. Why does it matter? (the implication, without overclaiming)

Use an analogy or concrete example where it earns its place, when a mechanism is genuinely hard to grasp otherwise. Not decoratively.

**Key takeaways**: only when the content is genuinely list-shaped. Use these symbols only:
- ✅ finding or advantage
- 💡 idea or insight
- 1️⃣ 2️⃣ ordered points
- 🎯 final conclusion

Don't bullet a post that reads better as prose.

**Reflection**: one short paragraph, the user's own take, in the voice of an AI engineer or researcher who cares about practical adoption. This is the one place first person is allowed, and it must clearly be commentary, not a claim of authorship over the research.

**Closing**: a thought-provoking question or an invitation to discuss. Then, exactly this line:

```
Link in the comments 👇
```

**Hashtags**: exactly 3, all in English, on their own line at the end. Highly specific to the content, not generic (`#AI` is weak; `#MechanisticInterpretability` is useful).

## Tone

Professional, friendly, inspiring, readable. Reject: clickbait, hype, marketing register, and academic stiffness. The test: would a competent engineer who *has* read the paper find the post accurate, and would one who hasn't find it clear?

Bold only where it actually aids scanning. Emojis sparingly, and only the symbols listed above.

## Before sending, check

- Every number in the post matches the source exactly, with its benchmark or condition.
- No finding appears that the source doesn't state.
- Attribution is third person outside the Reflection (unless the user is an author).
- Every affiliation named appears in the source, and the work is not called "new" unless it is.
- The post is 200–300 words, ends with `Link in the comments 👇`, then exactly 3 English hashtags.
- The three hooks differ in angle, and the post opens with the strongest one.
