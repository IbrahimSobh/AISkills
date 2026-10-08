---
name: tweet-post
description: Write a tweet / X post about any kind of technical content — something Ibrahim built (a skill, tool, CLI, project), a research paper or finding, a technical insight, or a project update. Use whenever he asks for a "tweet", "tweet-like post", "X post", or to "post this on Twitter/X," in English or Arabic — even if he gives a different word/character limit. Also trigger when he pastes a SKILL.md, README, paper abstract, or technical write-up and asks to "tweet about it" or "announce it on X." Do NOT use for LinkedIn posts or any longer-form social post (LinkedIn has a different pacing and no hashtag/word-count contract — ask him what he wants instead of reusing this skill's constraints) or for long-form technical explainers (use technical-article-writer instead). This skill is specifically for a single tweet-length X post, on any technical subject matter.
---

# Tweet Post

## Overview

Ibrahim wants tweet-length technical posts written as a personal engineering
narrative compressed to X-post size, not marketing copy and not a generic listy
summary. This applies whatever the subject is — something he built, a research
paper or finding, a technical insight — the compression discipline and
narrative arc are the same regardless of content type; only the voice changes
(see Voice, below). The single biggest failure mode is treating "tweet-like" as
*only* a brevity instruction and losing the narrative arc in the process — a
tweet under this skill still has a hook, a turn, and a close that echoes it;
it's just all of that packed into ~110 words instead of a paragraph each. The
whole point of this skill is to hit that density without collapsing into a bare
feature list.

This skill is scoped to X/Twitter only. If Ibrahim asks for a LinkedIn post or
something longer, that's a different pacing and structure (more room per beat,
no hashtag convention) — don't force this skill's word cap or hashtags onto it;
ask what length/platform he actually wants.

## The structure

Every post follows this shape, in order:

1. **Hook** — one or two sentences naming a broader problem, risk, or insight in
   the *field*, not the specific thing built. The reader should recognize the pain
   before they know a solution exists. Never open by describing the artifact.
2. **Turn** — one sentence pivoting from problem to reveal: "To address this,
   here's X" when Ibrahim built the thing, or "A recent paper/team addresses
   this by X" when the post covers someone else's work. Either way this is the
   bridge from problem to solution — lead with the artifact or finding, not a
   first-person construction verb.
3. **Substance** — narrate what the thing does or what was found, in the voice
   that matches who did the work (see Voice, below). Bullets or emoji markers
   are fine here for scannability (pick emoji that match the content, not
   generic decoration) — keep each line terse.
4. **Reasoning** — state at least one explicit design decision (if Ibrahim built
   it) or one notable methodological choice / implication (if it's someone
   else's work), and the thinking behind it — e.g., "One principle I
   intentionally included is..." or "What's notable is that the authors chose
   to...". This is the sentence that makes the post read as engineering
   judgment, not a spec sheet or a press release. Don't skip this — it's the
   most commonly dropped section and the one that matters most.
5. **Systemic note** (optional) — one sentence on how this fits a larger workflow,
   if relevant (e.g., how it's meant to be used alongside other tools or people).
6. **Close** — a generalized, aphoristic sentence that echoes the *opening hook's*
   theme. Not a punchline about the specific feature. The post should feel like it
   completes an argument, not that it ends a list.

## Voice

Voice depends on whose work the post describes — this is the one thing that
changes across content types, everything else in the structure stays fixed.

- **If Ibrahim built the thing**: first person for the substance and reasoning
  sections ("I designed," "I included") — this is him announcing something he
  made, not third-party marketing copy describing a product. The one exception
  is the Turn/bridge sentence itself, which uses "Here's X" rather than "I
  built X" — everything downstream of that bridge stays in first-person
  ownership voice.
- **If the post covers someone else's work** — a research paper, a lab's
  finding, a third party's project — attribution stays third person throughout
  the substance and reasoning sections: `researchers at X`, `the paper's
  authors`, `Anthropic's team`, never "I" as if Ibrahim did the work. The only
  first-person voice allowed here is a short reflection if Ibrahim wants to add
  his own take — and it must read clearly as commentary *on* the work, not a
  claim of authorship over it.
- Exception within the Reasoning section: when stating a hard design
  constraint (something made mandatory/non-optional/required), phrase the
  constraint itself passively — "X is made non-optional," not "I made X
  non-optional." The rest of the reasoning sentence (the justification/"why")
  stays in whatever voice fits naturally. E.g. "Checkpoints are made
  non-optional on purpose — a step an agent can skip, it eventually skips
  exactly when it matters."
- No warm-up phrases, no hedging — consistent with his general style. But this is
  one context where a reflective, slightly philosophical tone is *wanted*, unlike
  his terser preference for direct technical answers elsewhere.
- Emoji-as-bullet-markers are acceptable here for scannability, even though his
  general preference is anti-decoration. Social/announcement posts are the
  exception.

## Accuracy, when the post covers someone else's work

These apply whenever the subject is a paper, finding, or project Ibrahim
didn't build himself — they don't apply to his own announcements, where he's
the authority on what he built.

- **Never invent findings.** Work only from what's actually provided (the
  paper, abstract, or write-up). Infer the post's *structure*, never the
  substance. If something important is missing, say so and ask rather than
  filling the gap plausibly.
- **Preserve numbers exactly.** A reported 12% improvement stays 12%, on the
  specific benchmark it was measured on — never rounded into a vibe, never
  generalized from one dataset into a claim about everything.
- **Don't upgrade correlation into causation**, and don't upgrade "on this
  benchmark, under these conditions" into "in general." If the source hedges,
  the post hedges.
- **Flag limitations that change the interpretation** in one honest clause,
  not a disclaimer dump — e.g. if a result only holds at large scale, or was
  only tested in one language.

## Language level (A2–B1)

Write the output at **CEFR A2–B1 English**. This constrains sentence
construction, not the ideas. Keep the thinking hard and the sentences easy.

- Sentences mostly under 20 words. One idea per sentence.
- Active voice. Subject-verb-object order.
- Common everyday verbs: "use" not "utilize", "start" not "commence", "show"
  not "demonstrate", "so" not "thereby".
- Simple connectors only: and, but, so, because, when, if, however, which
  means, for example. Avoid "whereby", "insofar as", "notwithstanding",
  "albeit".
- No idioms, no decorative metaphor, no phrasal verbs where a plain verb
  exists.
- Don't stack subordinate clauses. Split into two sentences instead.

**Exempt from the level cap.** These are not "advanced English" and must not be
simplified away:

- Technical terms, jargon, and proper nouns (LLM, non-deterministic, RLHF,
  DDIM, Anthropic, ContentRouter).
- Code, commands, file paths, API and model names.
- Exact numbers, units, dataset and benchmark names.
- Verbatim quoted text from a source.

CEFR measures general language, not domain vocabulary. A sentence can be A2 in
grammar and fully technical in content. That is the target.

**Precision outranks the level.** If a simpler sentence would change the
meaning, weaken a hedge, or drop a caveat, keep the harder construction and
move on. Never trade accuracy for reading level.

This covers every beat: hook, turn, substance bullets, reasoning, and close.
The aphoristic close and its antithesis structure are still wanted — an
em-dash contrast is a rhetorical device, not grammatical complexity. Just keep
each half of it short and plain.

On Arabic posts, apply the fusha rules already in the Language section instead.
CEFR applies to the English output only.

## Length & hashtags

Target **100–120 words**, plus **2–3 hashtags** on their own line at the end.
This is the standard output for this skill. Fit the six-part structure into that
budget by compressing every section, not by dropping one:

- Hook: 1 sentence.
- Turn: 1 sentence.
- Substance: 2–4 short bullets (or one dense sentence if bullets don't fit) —
  name the dimensions/features, don't explain each one.
- Reasoning: 1 sentence. This is the section most likely to get cut under
  length pressure — don't cut it. A post that hits 110 words but drops the
  design-philosophy line is worse than one that runs slightly long but keeps it.
- Close: 1 sentence, echoing the hook.
- Hashtags: 2–3, specific to the content — not generic filler like #innovation
  or #tech. Mix a broad field tag with a specific one, e.g. #AI #CodeReview
  #SoftwareEngineering. Keep hashtags in English even on Arabic posts,
  consistent with keeping English tech terms untranslated.

**If Ibrahim gives a different explicit length** — a real X/Twitter character
limit (~280 chars), "make it longer," or a request for the full narrative
version — follow that instead. His latest explicit instruction always overrides
this default, and skip hashtags if he's asked for a hard character limit that
can't fit them.

## Language

- Default to English unless Ibrahim writes in Arabic or asks for it.
- Arabic: use standard/formal Arabic (fusha), not Egyptian ammiya, unless told
  otherwise. Keep English tech terms untranslated (Agentic AI, Skill, Claude,
  etc.). Same hook → turn → substance → reasoning → close shape applies.
- If Ibrahim wants an Arabic LinkedIn post (not a tweet) built around a
  research paper, `linkedin-arabic-science-post` is the right skill for that
  longer, LinkedIn-paced format — this skill only covers the tweet-length case,
  regardless of subject matter.
- If Ibrahim actually wants a LinkedIn post rather than a tweet, don't use this
  skill's word cap or hashtag rule for it — LinkedIn posts run longer with no
  hashtag convention. Confirm which platform he means if it's ambiguous.

## Example (~110 words + hashtags)

This is the calibration example — match this shape, register, and length:

> Most agent failures aren't reasoning failures — they're state failures. An
> agent forgets a decision, second-guesses itself mid-task, or drifts from the
> plan with nothing to catch it.
>
> To fix this, here's a Sequential Orchestrator: a single-model framework that
> runs execution in strict sequence, gated by mandatory checkpoints.
>
> 🔨 Builder mode commits to an approach
> 🔍 Critic mode reviews it against the original intent
> 📍 A fixed trace vocabulary keeps the reasoning legible after the fact
>
> Checkpoints are made non-optional on purpose — a step an agent can skip, it
> eventually skips exactly when it matters.
>
> Reliable agents aren't the best reasoners. They're the ones that know when to
> stop and check their own work.
>
> #AgenticAI #LLM #AIEngineering

Note how the close ("the ones that know when to stop and check their own work")
answers the open ("aren't reasoning failures, they're state failures") — that
mirroring, at tweet length, is the tell of a well-formed post under this skill.

### Example, someone else's work (~105 words + hashtags)

Same shape, third-person attribution throughout the substance and reasoning:

> Most claims about model scale assume bigger always means better. The data
> rarely backs that up cleanly.
>
> A new paper from a DeepMind team tests that assumption directly, across
> benchmark families rather than a single leaderboard.
>
> 📊 Gains past 30B parameters flatten on reasoning tasks
> 📊 They keep climbing on retrieval-heavy tasks
> 🔍 The split holds across three model families, not just one
>
> What's notable is that the authors controlled for training data volume, not
> just parameter count, so the split isn't just an artifact of more tokens.
>
> Scale isn't one lever. It's several, and they don't move together.
>
> #MachineLearning #ScalingLaws #DeepLearning

## Anti-patterns — don't do these

- Opening with the artifact/finding ("Here's a skill that..." / "A new paper
  shows...") instead of the field-level problem.
- Using "I built a..." as the Turn sentence instead of "Here's..." — the bridge
  should present the artifact, not lead with a first-person construction verb.
- For Ibrahim's own builds: third-person/descriptive voice ("it evaluates,"
  "it doesn't just flag") instead of first-person ownership voice ("I designed
  it to evaluate").
- For someone else's work: first-person voice ("I found," "I built") as if
  Ibrahim did the research or built the thing — attribution has to stay
  third-person (`the authors`, `the team`) outside of an explicitly marked
  reflection.
- Closing on a punchy feature-specific one-liner instead of echoing the opening
  hook's theme.
- Compressing hard to hit a stated word-count ask at the cost of dropping the
  reasoning/philosophy sentence — that sentence is the one thing a generic
  summary can't fake.
- Listing features without explaining the design decision behind at least one of
  them.
- Running past 120 words "to fit everything in" instead of compressing the
  substance section — the reasoning and close matter more than feature
  completeness.
- Generic or filler hashtags (#innovation, #tech, #AI alone with nothing
  specific) instead of tags tied to the actual content.
- Packing the hook or close into one long clause chain to sound profound —
  the antithesis works better in two short sentences than one long one.
- Writing a LinkedIn-length post (200+ words, multiple paragraphs, no hashtags)
  when Ibrahim asked for a tweet — the platforms have different pacing; don't
  reuse LinkedIn habits here just because the underlying narrative shape is
  similar.
