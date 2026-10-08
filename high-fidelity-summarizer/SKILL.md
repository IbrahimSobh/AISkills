---
name: high-fidelity-summarizer
description: Compress technical, legal, financial, or analytical text into a dense summary that keeps every named entity, number, claim, and the source's structural/chronological flow — but rewrites the prose. Wording is carried over literally by exception only (proper nouns, product names, acronyms, file names, terms of art), plus at most one verbatim quote under 15 words. No outside information, no simplification. Length targets 25% of the source word count. Use whenever the user asks to "summarize," "condense," "compress," or "shorten" a document, article, contract, report, paper, or transcript — especially where factual precision outranks readability and the summary must stand in as a proxy for the original. Do NOT use for making text easier to understand (that's the simplifier skill — it preserves length and reduces difficulty; this preserves difficulty and reduces length). Do NOT use when the user wants the original's shape and wording kept for study with no length target (that's content-highlighter).
---

# High-Fidelity Summarizer

A compression skill. The summary must work as a reliable technical/legal proxy for the source — someone reading only the summary should walk away with the same names, numbers, and logical progression they'd get from the full text, just faster.

Fidelity here means **fidelity to the facts and the structure, not to the sentences.** The prose is rewritten; the entities, figures, claims, and order are not.

## Why these constraints exist

- **Preserve meaning, not phrasing** — named things must survive intact, because swapping a synonym for an established term breaks the summary's reliability as a proxy. The connective prose around them carries no such load, so it gets rewritten in fresh, tighter wording.
- **Stay non-displacive** — a summary built from copied sentences is a reproduction, not a summary. Rewriting is what makes it a compression.
- **Maximize density** — every sentence should be pulling weight. Cut connective tissue and restatement, not substance.
- **Minimize cognitive load** — the reader should absorb the author's actual logical path, not Claude's reorganization of it.

## Hard constraints

1. **Length**: target **25% of the source word count**, inside a band of **22%–28%**. Below 22% is over-compressed (drops substance); above 28% is under-compressed. There is no exception for short or long inputs.
   - **Convert the percentage to a word number before drafting.** A percentage is not something you can aim at while writing; a word count is. Count the source, then compute the target and the band as concrete numbers — e.g. source 1,240 words → target 310, band 273–347 — and write to that number.
   - **Revision is bounded. Never loop.** See *Length policy* below for the exact rule.

2. **Literal by exception only**: the default is rewriting. A fixed, closed list of items is carried across exactly as written; everything else is expressed in new wording.

   Carried over literally:
   - Proper nouns (people, organizations, places).
   - Product, tool, model, and library names (Claude Code, MCP).
   - Acronyms and initialisms (RLHF, SLA, EBITDA).
   - File names, paths, commands, code identifiers (AGENTS.md, `--no-cache`).
   - Terms of art — the field's defined vocabulary, where a synonym would change or blur the meaning (greenfield/brownfield, force majeure, gradient checkpointing).
   - Exact numbers, dates, units, metrics, and the citation form of a quoted figure.

   Everything else is rewritten: verbs, framing, transitions, clause order, sentence shapes, metaphors, examples' phrasing. Do not lift a sentence and delete its middle — that is copying with cuts, not summarizing. If you find yourself reusing more than a few consecutive words of the source outside the exception list, rewrite that line.

   Borderline call: if unsure whether a phrase is a term of art or just the author's wording, ask whether a reader in that field would recognize it as a defined term. If not, rewrite it.

3. **One anchor quote, max**: reserve **at most one** verbatim quote for the entire summary — **under 15 words** — placed at the single point where exact wording is load-bearing (a stat, a defined term, a specific claim, a memorable line). Mark it clearly, wrapped in quotes. Every other sentence in the output must be rewritten.
   - The quote is optional. If no single line is truly load-bearing, use none.
   - If the source is very short, skip the quote entirely — a 15-word quote from a short source is displacive, not a summary.
   - The one-quote budget is per source. If several sources are summarized in one request, one quote each; if a source was already quoted earlier in the conversation, don't quote it again.
   - Never split the budget into several short quotes. Two five-word quotes are two quotes.

4. **Zero outside information**: no added facts, no filled-in context, no inference beyond what's stated. If the source is ambiguous, the summary stays ambiguous too. Rewriting the wording never licenses changing, sharpening, or resolving a claim.

5. **Tone alignment**: match the source's register — formal, technical, urgent, analytical, whatever it is. Don't warm it up or flatten it. New wording, same voice.

6. **Structural mirroring**: preserve the source's thematic/chronological order. If the source goes A → B → C, the summary goes A → B → C, in proportion to how much space each section had.

7. **Format mirroring**: the summary's surface formatting follows the source's, not a default. If the source is organized under headers, numbered steps, or bullet lists, render the summary the same way — headers stay headers, ordered lists stay ordered lists. If the source is continuous prose, the summary stays continuous prose. Never impose bullets/headers onto prose source material, and never flatten a genuinely structured source into a single block of prose. Header text itself may be carried over verbatim; it is a label, not prose.

## Execution steps

1. **Budget** — count the source with `wc -w`, then compute and write down three numbers: target (25%), floor (22%), ceiling (28%). Everything after this aims at the target number, not at a percentage.
2. **Map the structure** — identify the source's sections/blocks, the order they appear in, and the format each is in (prose paragraph, numbered steps, bullet list, table, header hierarchy).
3. **Extract per block** — pull the core claim and supporting pillars from each block, and list the exception-list items in it (names, acronyms, file names, terms of art, figures) that must survive. Don't skip a block just because it's short; represent it proportionally. Allocate each block a share of the target word budget, proportional to the space it had in the source.
4. **Draft once, to the target number** — write in your own sentences, following the mapped order and the source's tone, dropping in the exception-list items exactly as the source spells them. Pick the anchor quote now, if one is warranted.
5. **Count** — run `scripts/check_summary.py`. This is the single source of truth for the numbers you report.
6. **Correct at most once, sized to the gap** — if the count is in band, stop here and go to step 7. If not, trim or restore roughly the number of words you are off by; do not rewrite the summary. Over the ceiling: cut adjectives, connective phrases, hedging, and restatement — never entities, numbers, or structural steps. Under the floor: restore detail (supporting figures, qualifiers, the blocks you compressed hardest), never filler. Then count again. **See *Length policy* for when to stop.**
7. **Verify** — confirm every proper noun/acronym/file name/term of art matches the source exactly; confirm nothing outside that list was copied verbatim beyond the single anchor quote; confirm the quote is one, under 15 words, and marked; confirm no external claim slipped in; confirm section order and formatting match. This is a read-through, not a rewrite.
8. **Report** — append the separator and the two-line word-count/percentage report described in **Output format**, using the numbers from step 5 or 6.

## Length policy

- **Draft once. Correct at most once. Hard cap: two counted passes.**
- After the correction pass, if the summary is **within 5 percentage points of the band** (i.e. 17%–33%), **ship it as-is.** Do not attempt a third pass.
- Only if it is **more than 5 points outside** the band (below 17% or above 33%) does a second correction pass run. Then ship regardless of the result.
- An out-of-band result is shipped honestly: the mandatory report line shows the real number. A visible 29.4% is acceptable; burning passes to reach 27.9% is not.
- Never re-draft from scratch to fix length. Trimming and restoring are edits, not rewrites.

## Counting

`scripts/check_summary.py` gives the word count, the compression ratio, and a flagged list of capitalized terms/acronyms from the source so you can eyeball whether the exception-list items survived. It doesn't replace the step 7 read-through for tone, order, over-copying, or hallucination — it only catches what's mechanically countable.

**The final reported numbers must come from this script, not from estimation.** Expected cost is 2 script calls per summary (one for the source budget, one for the count), 3 in the rare second-correction case.

```bash
wc -w source.txt                                                  # step 1, budget
python3 scripts/check_summary.py --source source.txt --summary summary.txt   # steps 5-6
```

## Output format

Return the summary itself with no "Here's your summary:" preamble and no meta-commentary inside it. Match the summary's language to the source's language, and match its formatting per the format-mirroring rule above.

Then **always** close with a `---` line separator followed by these two lines, in this order and nothing else:

```
---
Summary number of words: <N>
Summary size percentage of the original : <P>%
```

- `<N>` is the whitespace-separated word count of the summary text only — not counting the separator or these two report lines.
- `<P>` is `<N>` / source word count, as a percentage rounded to one decimal (e.g. `25.4%`). Report the real number even when it falls outside 22%–28% — an honest out-of-band figure is correct output under *Length policy*. Never adjust the reported number to look in band.
- These two lines are part of the required output, not optional meta-commentary. The report is always shown, whether or not the user asked for it. If the user also asked for the full verification data, append that below these two lines.
- Write the labels exactly as shown, including the space before the colon on the second line.
