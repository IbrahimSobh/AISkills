---
name: fact-checker
description: Verify the factual claims in a piece of text — an article, post, transcript, list of statements, or anything else the user pastes in — and return a Markdown table classifying each claim as Correct, Partially Correct, or Incorrect, backed by cited sources. Trigger this whenever the user asks to "fact-check", "verify", "check the accuracy of", "is this true", or shares a draft/post/claim and wants to know if the numbers, dates, quotes, or statements in it hold up. Works in any language — match the output language to the language of the claims being checked (e.g. English claims get an English table, Arabic claims get an Arabic table).
---

# Fact Checker

Verify factual claims against reputable sources and report the verdict in a standard table. The value of this skill is in cited, sourced verification — not recall — so every claim gets checked against live sources, even ones that seem obviously true or false.

## Step 1 — Identify the claims

Pull out every distinct, checkable factual statement from the input: something with a truth value that evidence can confirm or refute (a number, a date, an attribution, an event, a mechanism). Leave out opinions, predictions, and subjective framing — they have no evidence to check against.

- If the input contains no checkable claims, or a statement is too vague to verify as written (undefined scope, no clear referent), don't guess at what was meant — ask the user to clarify or restate it in checkable form, and don't produce a table until you have something concrete to check.
- If the input is a mix of checkable claims and other content (opinions, hedges, predictions), check only the checkable parts. Mention once, outside the table, that the rest was excluded and why — don't caveat this per row.

## Step 2 — Research each claim

Check every claim individually against current sources — internal knowledge alone isn't sufficient, since the whole point is a cited verdict, not a recollection.

**Source priority:**
1. Academic/peer-reviewed publications
2. Government and international-body data (statistics agencies, .gov/.int sites, primary records)
3. Established news outlets with editorial standards

**Avoid as evidence:** personal blogs without citations, forums, social media posts, and aggregator/content-farm sites that repeat a claim without originating it.

For claims with a numeric or statistical component, prefer sources that report the actual figure over ones that only describe it qualitatively — the precision is usually the point of checking. Gather up to three sources per claim. If reputable sources genuinely disagree, that disagreement is part of the finding — reflect it in the verdict and evidence summary rather than silently picking a side.

## Step 3 — Classify

- **✅ Correct** — fully supported by the sources gathered.
- **🟡 Partially Correct** — some elements hold up, others don't (right in substance but wrong on a specific number, date, or attribution, for instance). State which part is which.
- **❌ Incorrect** — unsupported by, or contradicted by, the evidence.

## Step 4 — Output format

Structure the response exactly like this:

```
| Claim | Decision | Evidence & References |
|---|---|---|
| <claim as stated> | ✅ Correct | <1-2 sentence summary of what the evidence shows, with a specific figure/date if it strengthens the point> [1] |
| <claim as stated> | 🟡 Partially Correct | <what's right, what isn't> [2][3] |
| <claim as stated> | ❌ Incorrect | <what the evidence actually shows instead> [1] |

**Conclusion**
2-4 sentences on overall accuracy across everything checked (e.g. "3 of 4 claims fully verified; one overstated the reported growth rate.").

**References**
[1] [Source name/title](https://exact-url-of-the-page-cited)
[2] [Source name/title](https://exact-url-of-the-page-cited)
[3] [Source name/title](https://exact-url-of-the-page-cited)
```

Reference numbering: assign a number the first time a source is cited, then reuse that number anywhere else the same source supports a claim — don't renumber duplicates. Cite with bracket notation ([1], [2]) inside the table only; full URLs belong exclusively in the References list at the end.

Every reference must be a working markdown link — `[Source name/title](URL)` — not a bare source name and not a raw pasted URL. Use the exact page actually consulted (the specific article, report, or dataset), never a homepage, search-results page, or a guessed/reconstructed URL. If a source's real URL isn't available (e.g. it came from general knowledge rather than a specific fetched page), don't fabricate one — either omit that source from the numbered list or drop the claim's citation rather than inventing a link.

If nothing could be verified (everything in the input was ambiguous or non-factual), skip the table entirely and say plainly that clarification is needed, naming what's unclear.

## Step 5 — Offer a corrected version

If the table contains any 🟡 Partially Correct or ❌ Incorrect verdicts, ask the user — right after the table and conclusion — whether they want the original text corrected to reflect what the evidence shows. Don't produce the rewrite unprompted; it's an offer, not an automatic part of the deliverable.

If everything came back ✅ Correct, skip this step entirely — there's nothing to fix.

If the user says yes: reproduce the entire original input as a single corrected block, with the 🟡 and ❌ claims fixed to match the evidence. Everything else — correct claims, wording, tone, structure — stays as close to the original as possible; the goal is the same text with the flagged inaccuracies repaired in place, not a summary or excerpt.

The corrected block must read as clean, ordinary prose — as if it had been accurate from the start. Don't carry any trace of the fact-check into it: no ✅/🟡/❌ symbols, no verdict words ("Correct" / "Partially Correct" / "Incorrect"), and no "not X, actually Y" or "previously stated as..." framing. State the corrected fact plainly, the same way the rest of the passage states its facts — the corrected claim shouldn't be distinguishable in style from a claim that was already right. Any explanation of what was wrong belongs in the table above, not in this block.

## Style

- Neutral and professional — report what the evidence shows; don't editorialize about a claim being wrong.
- The Evidence & References cell is a summary, not a report: one to two sentences.
- Don't narrate the research process — which queries were run, which sources were checked and discarded, or any other internal reasoning. Only the verdict, the evidence summary, and the citations belong in the output.

## Language

Detect the language of the claims themselves (not any surrounding instructions the user gave in another language) and write the entire output — table, conclusion, and reference list — in that language. Arabic claims get a fusha table; English claims get an English table; match whatever the input uses.
