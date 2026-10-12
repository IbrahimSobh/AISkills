# skill-doctor

Reads an existing AI skill (a `SKILL.md` plus its scripts and references) and reports what it does, how it flows, whether it is well built, whether its claims hold up, and what to fix. It diagnoses and prescribes; actual edits are handed off to `skill-creator`. For anyone who wants a second opinion on a skill they own or inherited.

## When to use it
- You want a plain explanation of what a skill does and when it triggers.
- You want an audit of a skill's design quality and technical accuracy, with ranked fixes.
- You want a health rating before deciding whether to rework a skill.

## Example request
> Review the high-fidelity-summarizer skill and tell me how to improve it.

## Example output

**What it does:** Compresses technical, legal, financial, or analytical text to about 25% of its word count, keeping entities, figures, claims, and order while rewriting the prose.
**Why it exists:** Gives a summary that can stand in for the source, where precision matters more than readability. It keeps difficulty and cuts length (the opposite of `simplifier`).
**How it works:**
1. Count source words, compute target/floor/ceiling (25% / 22% / 28%).
2. Map the source's sections and formats.
3. Extract core claims and must-survive exact items per block, with a word budget each.
4. Draft once, in new wording, with at most one verbatim quote under 15 words.
5. Run `scripts/check_summary.py`, correct at most once (second pass only if outside 17%-33%).
6. Verify entities, order, format; append the two-line word-count report.

**When it triggers:** Requests to summarize, condense, compress, or shorten a document where factual precision outranks readability. Not for simplifying and not for study copies with no length target.

**Design quality**
- Pro: the description states what and when, with explicit exclusions; the body explains why for each constraint; the counting logic lives in a script.
- Pro: the bounded length policy ("Draft once. Correct at most once.") avoids revision loops.
- Con: the `description` points to `simplifier` and `content-highlighter`, but neither has a SKILL.md in this repo, so the overlap boundaries could not be checked.
- Con: no eval cases, although the output is largely mechanical (band, one quote, report format).

**Accuracy** (no external-world claims; `fact-checker` and `content-diagrams` were not invoked, so no fact-check verdicts are given and nothing was eyeballed)
- Verified by reading the script: `extract_terms` misses `20%` (`%\b` cannot match before a space; a test run returned only `$400M`, `3.5x`, and `Revenue`). It also never detects dates, units like `50 ms`, lowercase terms of art (`force majeure`), or flags like `--no-cache`, all of which the exception list names.
- Judgment: `scripts/check_summary.py` says "your 'core thesis + supporting pillars' from step 2", but extraction is step 3 in SKILL.md.
- Judgment: the script counts the whole file, while the reported `<N>` excludes the separator and report lines. SKILL.md never says to keep those lines out of `summary.txt`.
- Judgment: the script prints `LENGTH: FAIL` for 28%-33%, which the Length policy says to ship as-is. This is confusing but not wrong.

**Proposed enhancements**
1. [High impact] [domain] Fix the metric regex in `extract_terms` so `20%` is detected, and add dates and units (ms, GB, years).
2. [High impact] [design] Add an n-gram overlap check to `check_summary.py` for the "no copying beyond exceptions, one quote under 15 words" rule. Step 7 currently depends on a manual read-through.
3. [Med impact] [design] State that `summary.txt` must hold only the summary text (no `---` or report lines), or make the script strip them.
4. [Med impact] [design] Add 2-3 eval cases: short source, structured source, and an out-of-band result that ships honestly.
5. [Med impact] [design] Make the script's PASS/FAIL language match the Length policy (for example, "ship" for 17%-33%).
6. [Low impact] [domain] Correct the "step 2" reference in the script's output text.
7. [Low impact] [design] Say how to render tables, since format mirroring covers only headers, lists, and prose.

**Overall health: Good.** The workflow and constraints are carefully reasoned; the checker script under-delivers on the rules it is meant to enforce.

Chart skipped: the control flow is a linear pass with one bounded correction, which does not meet the skill's branching criteria.

_Last run: 2026-10-12 · Claude Sonnet 5.5_

## Install
```bash
cp -r skill-doctor ~/.claude/skills/
```
Full instructions for the agent: [SKILL.md](SKILL.md)
