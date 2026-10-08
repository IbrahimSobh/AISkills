---
name: skill-doctor
description: Diagnose an existing AI Skill (SKILL.md) — plain explanation of what/why/how/when, an optional workflow diagram, a two-lane review (design quality + technical/domain accuracy), and ranked enhancement suggestions. Hands off actual edits to skill-creator rather than duplicating its update logic. Use whenever the user wants to "understand," "explain," "review," "audit," "evaluate," or "get a second opinion on" a skill they already have (their own or someone else's) — e.g. "what does this skill do," "is this skill any good," "how could this be better," "diagram how this skill works." Not for building a new skill from scratch or running trigger-optimization loops — route those to skill-creator instead.
---

# Skill Doctor

Reads an existing skill and reports back: what it does, how it flows, whether it's well-built, whether what it teaches Claude to do is actually correct, and what to fix. Does not write the fix itself — that's skill-creator's job.

## Scope

This is a read/diagnose skill, not a build skill. It never edits a SKILL.md directly. When the diagnosis calls for changes, stop at "here's the prescription" and tell the user to invoke skill-creator to implement — don't reimplement its update mechanics (name preservation, writable-copy-before-edit, packaging) here.

## Input

Read the target skill's SKILL.md in full, plus anything its instructions point to (`scripts/`, `references/`, `assets/`) that's relevant to the phase being run. A path or a name is enough to locate it; don't ask the user to paste the file if it's already on disk.

## Which phases to run

Default to the full report (Diagnose → Examine → Proposed enhancements) for any broad ask ("review this skill," "give me the rundown," "audit this"). Run a single phase only when the user's ask is scoped to it ("just explain what this does," "only check if the AUTOSAR steps are accurate"). Chart and Treat are opt-in — see their sections.

## Phase 1 — Diagnose (explain)

Output exactly this shape, no more than ~150 words total:

```
**What it does:** <one line, functional>
**Why it exists:** <the gap it fills, 1-2 sentences>
**How it works:** <numbered list of the core steps — the actual control flow, not a paraphrase of the SKILL.md's section headers>
**When it triggers:** <the trigger conditions, restated plainly, not copy-pasted from the description field>
```

## Phase 2 — Chart (diagram, opt-in)

Only produce this when the user asks for a "diagram"/"visual"/"plot," or the skill's control flow has real branching/looping (conditional paths, an iterate-until-satisfied loop, parallel subagent fan-out) that prose genuinely struggles to convey. Skip it for simple linear skills — a 4-step straight line doesn't need a picture, even a rule-heavy one: a single read-apply-rules-output pass (many rules, one pass) still doesn't qualify. A phase-selection branch combined with multi-target delegation (skill-doctor's own shape, for instance) does.

When producing one: delegate to `content-diagrams`, requesting its **in-article explanatory diagram** treatment — let it own the exact sizing/format spec rather than restating it here, since that's its detail to maintain. Brief it with the skill's actual control-flow shape — pipeline, decision tree, iteration loop, fan-out/fan-in — so the motif matches the real structure instead of defaulting to a generic flowchart. If `content-diagrams` isn't available as a tool in this session, say so and skip the diagram rather than sketching one yourself.

## Phase 3 — Examine (review)

Two independent lanes. Keep each to a tight pros/cons list — bullets, not paragraphs.

**Design-quality lane** (self-contained; check against these, drawn from skill-creator's own authoring principles):
- Trigger description: specific and appropriately assertive, covers both *what* and *when* in the description field itself
- Progressive disclosure: SKILL.md body reasonably lean, with heavy content pushed to `scripts/`/`references/` rather than bloating the body
- Scope discipline: does it overlap or conflict with another installed skill's territory
- Test coverage: does it have (or plainly need) verifiable eval cases, or is its output too subjective for that
- Writing style: imperative, explains *why* rather than leaning on rigid ALL-CAPS musts

**Domain/technical-accuracy lane:**
- Split checkable claims by what actually verifies them — these are different jobs, don't route both through the same tool:
  - **Claims about the external world** (version numbers, named APIs/tools/standards, general technical facts) → hand to `fact-checker`, report its verdicts. If `fact-checker` isn't available as a tool in this session, say so and skip this part rather than eyeballing a verdict yourself.
  - **Claims about a sibling skill's own documented behavior** (e.g. "hands off to skill-creator's update path," "matches content-diagrams' sizing convention") → verify by reading that sibling skill's file directly. Fact-checker has no web-sourced answer for another skill's internal instructions.
- Separately, judge what neither of the above covers: does the procedure itself hold together logically — step order, missing edge cases, a workflow that wouldn't actually produce the claimed output. Flag these as your own judgment calls, clearly separated from the two verified categories above.
- If a skill has no checkable claims of any kind (pure style/methodology skills, for instance), say so plainly instead of forcing a fact-checker call or manufacturing a verdict.

## Phase 4 — Proposed enhancements

Ranked list, each entry one line: `[High/Med/Low impact] [design | domain] <the fix>`. Rank by impact, not by which lane found it. Cap at 5–7 items — if Examine surfaced more than that, keep only the ones that actually change behavior or correctness, not stylistic nitpicks.

Close the phase with one overall health rating: **Poor / Fair / Good / Very good / Excellent**, plus a single sentence naming what's driving it. This is a holistic call on the skill as a whole — weigh Examine's findings against how much the enhancement list actually matters, not a mechanical average of bullet counts. A skill with one high-impact gap can rate lower than one with several trivial ones.

## Phase 5 — Treat (implement, opt-in)

Only if the user says to go ahead ("make these changes," "update it," "fix #2 and #4"). Don't implement directly, and don't restate skill-creator's update mechanics here either — that's a second copy of logic that will drift the moment skill-creator's own instructions change. Tell the user you're handing off, then invoke `skill-creator` and follow whatever its current update-an-existing-skill instructions say. If skill-creator isn't available as a tool in this session, say so and stop rather than editing the skill yourself.

## Output discipline

- Every phase output must be accurate over comprehensive — if a claim can't be verified, say so rather than filling the gap with a plausible-sounding guess.
- No section is mandatory beyond what was asked for or what "full report" requires. Don't pad Diagnose with restated frontmatter, don't pad Examine with restating the skill's own text back at the user.
- If a phase has nothing to report (e.g. Proposed enhancements finds no real issues), say that in one line instead of manufacturing filler suggestions.
