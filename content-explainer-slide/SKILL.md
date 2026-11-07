---
name: content-explainer-slide
description: Turn a technical input (an experiment and its results, a paper, a pipeline, an algorithm, a system change, a benchmark) into ONE story-style explainer slide — a 16:9 image of 3–6 numbered cards (discovery → problem → method → where the numbers come from → result + lesson) that a junior engineer understands at first read, with traceable numbers, a visible WHY per method step, and an honest result. Use this whenever the user asks for "one slide", "a slide that explains", "a story image", "an explainer image/figure", "a LinkedIn image for this result/paper/experiment", "a visual summary of how X works and what it achieved", or says "make the steps clear, as a story" — even if they don't say "slide". Also use it to review or fix an existing explainer slide. Do NOT use for plain box-and-arrow architecture or concept diagrams (use content-diagrams or diagram-design), Mermaid diagrams (content-mermaid), multi-slide decks (pptx), a single data chart (dataviz), or animating a finished figure (figure-animator).
---

# Content Explainer Slide

Builds one image that tells the story of a technical piece of work: what was noticed, what was wrong, what was done and why each step works, where every number comes from, and what it achieved and taught.

The bar is **100% clear and intuitive for a junior engineer, not 100% detailed.** That bar comes from real review rounds: each time a term was undefined, a number had no visible origin, a step's reason was hidden in a footnote, or a card had an empty area, the reader came back with "what is this?", "where did 30 come from?", "why does that work?" — and the slide needed another round. Everything below exists to answer those questions *on the slide* before the reader has to ask.

A worked example of a finished slide plan (a neural-network "neuron surgery" experiment) is in `references/worked-example.md`. Read it once before planning your first slide; it shows what each card looks like when the rules are applied.

## Step 0 — Ask the output format, then build a fact sheet

### Ask the format (once, before drawing)

Ask the user which output format they want, unless they already said:

- **PNG via matplotlib (Python)** — best when the input has data, models, logs or result files, because a script can compute every number on the slide straight from those files (no hand-typed numbers). Also exports a JPG copy.
- **HTML/SVG page rendered to PNG** — best when the input is text only (a paper, a doc, notes), or when typography and layout polish matter more than computing numbers. Rendered to PNG with headless Chrome/Edge.
- **Both** — same slide plan, two renderings.

State your recommendation with the reason (data input → matplotlib; text input → HTML). If the user cannot be asked (an automated run), pick by that rule and say which one you chose and why.

### Build the fact sheet

Before designing anything, list every fact the slide may use. For each fact record:

| fact | value | measured on (which data / which section) | source (file + script, or paper page/table) |
|---|---|---|---|

Then:

- **Cross-check facts** against each other and against any draft text (a post, an abstract, a README). Resolve every mismatch now — a slide that says 38 while the post says 36 destroys trust, and these mismatches usually come from two places computing "the same" number differently (different sample size, different threshold).
- **Record the data split**: what was used to *build* the method vs. what was held back to *test* it. The slide has to say this, because "does the result hold on data it never saw?" is the first question a technical reader asks.
- **Two modes:**
  - *Data mode* (results, models, CSVs, logs exist): the drawing script loads them and computes every number at render time.
  - *Source mode* (text only): every number is copied from the source and the fact sheet cites where (page, table, figure). Do not invent or round numbers beyond what the source states.

Save the fact sheet next to the slide (`<name>_facts.md`) so later edits stay consistent.

## Step 1 — Find the story (3–6 numbered cards)

Write one sentence answering each question. Each answer becomes one card:

1. **Discovery / context** — what was noticed, or what the setting is.
2. **Problem** — what is wrong or missing, *measured*. If there are several problems, name them (Problem A, Problem B). State what is targeted **and what is deliberately not targeted, with the reason** — a reader who sees a weak item in the chart and no explanation assumes a mistake.
3. **Method** — the recipe for *one* case, as steps.
4. **From one case to all cases** — how the recipe was applied everywhere, the rules that decided how many, and the counts. Pair each fix with the problem it solves ("Fix A → Problem A").
5. **Result + lesson** — what changed, how sure we are, what it teaches.

Merge cards that say the same thing (redundant cards were removed in review every time). For a small input, cards 3 and 4 may merge, or the slide can be 3 cards: problem → method → result. Never more than 6 — beyond that it is a deck, not a slide.

## Step 2 — Headline

One or two lines across the top: a surprising fact + the action taken, e.g. "N of the M parts were doing nothing. So they got a job." The headline is what makes someone stop scrolling; the cards are what make them trust it. Headline numbers come from the fact sheet / the script variables, never typed by hand.

## Step 3 — Card skeleton (same for every card)

- **Number + accent colour.** Each card has a big number (1–5) and its own accent colour, used for its border and highlights. Numbers give reading order; colours let later cards point back ("the 11 detectors from card 4").
- **Title = the question the card answers.**
- **One bold takeaway sentence = the answer.**
- **One main figure.** The method card may use a grid of step cells; the result card may use a chart plus an explanation panel.
- **Data label** — which data this card uses and *why that data* ("18,000 of 60,000 training images (30%) — the rest kept unseen so the final check is fair").
- **Short footnote** — caveats only. Reasoning never goes in the footnote (see Step 4).

## Step 4 — Method card: WHAT / picture / WHY cells

Split the method into 3–5 numbered cells (a 2×2 grid when there are 4). Every cell has the same three bands, top to bottom:

1. **Caption (WHAT)** — one concrete action that says *what is compared with what*: "Compare a NEW image (one it never saw) with the pattern from step 2", not "it gets matched".
2. **Picture** — built from **real examples from the data or source**: actual inputs, the actual intermediate result, actual scores. Real examples are what make an abstract step believable; a generic icon teaches nothing.
3. **WHY box** — full width, fixed height, visibly styled (tinted background, "WHY?" label). It says why the step works.

The WHY must be in the picture, prominently. In review, reasoning placed in footnotes was missed every time and the reader had to ask repeatedly. Inside the cells, answer the questions readers will ask:

- *Why this choice instead of the obvious one?* (e.g. why subtract the average of the correct class)
- *What does this NOT affect, and why not?* (e.g. "it can only lower '3'; if another class already wins, nothing changes")

Show the mechanism as **before → after**: a small panel of scores/states before, an arrow, the panel after, with ✓/✗ on the winner and a short note on the arrow ("the 2nd-highest wins"). If a panel title does not fit below it, put it beside it.

If a picture simplifies reality (it shows pixels, while the real computation uses internal features), say so in the footnote — honesty about simplification costs one line and prevents a "that's not how it works" comment.

Mark a worked example as **"Example:"** and state the general rule ("same recipe for all 30 detectors"), otherwise readers think the method only covers that one case.

## Step 5 — Make every number traceable

- Show each number's origin as a visible chain: "21 examples → 3 styles → 3 detectors", "11 + 19 = 30 of 36 (6 spare)". Totals must visibly add up, and leftovers need a reason.
- State the **selection rules and thresholds** that produced counts ("a style needs ≥2 examples", "mistakes with <3 examples skipped as too few to learn").
- If data came from different sources (labelled vs. mined, measured vs. estimated), show it visually (dark vs. light bars) with a legend.
- Explain any notation the first time it appears ("×N = N style detectors for that mistake").
- In data mode the script computes every number; text strings use the variables (f-strings / template values). Hand-typed numbers drift out of sync with the data — this caused a real wrong slide.

## Step 6 — Honest result, every change explained

- Before → after on data **never used to build the method**; confirm on a second unused set when one exists.
- Give gains **and** losses ("34 fixed, 9 broken"). A result with only gains reads as cherry-picked.
- Statistics in plain words ("about 6 in a million by luck"), with the technical form small or in the footnote.
- A per-item change chart (after − before, coloured positive / negative / zero) **plus a "why each changed" panel**: why gains happened, why losses happened, any bonus side effect. Listing a loss without its reason invites the worst interpretation.

## Step 7 — Plain, consistent words

- Define every term at first use in a few plain words, or replace it with a plain word.
- One word per concept across the whole slide ("predicted" everywhere, never sometimes "answered").
- No internal nicknames ("Set A", "the twist", "lucky side effect", "×3") unless defined on the slide.
- Every claim must match its chart. If the chart shows something odd that the text doesn't address, address it.

## Step 8 — Legends and colour

- Every colour, shade, arrow and symbol is explained where it appears. Diverging images get "red = only in X, blue = only in Y".
- One colour meaning across the slide: e.g. red = problem/removed, green = fixed/good, grey = neutral. Card accent colours are separate from these semantic colours.
- Grouped items (styles of one mistake, variants of one step) sit in visible boxes so groups don't blur together.

## Step 9 — Conclusion and lesson banners

- **Conclusion banner** (green tint): what was shown, including its size and limits ("small but real gain that holds on new data").
- **Lesson banner** (bottom of slide): what the reader can carry to other problems.

## Step 10 — Layout

- 16:9 (e.g. 16×9 in at 150 dpi, or a 1600×900 px canvas). Cards read left→right in story order.
- Size cards by content — the method card is usually widest. No large empty areas: if a card has spare room, widen its chart or move its text panel into the space.
- No overlapping text; labels stay inside their boxes. Wrap long lines rather than shrinking fonts below phone readability (≈7.5 pt at 16×9 in is the floor).
- Read `references/matplotlib-recipes.md` (PNG) or `references/html-recipes.md` (HTML) for layout code. `scripts/slide_kit.py` provides matplotlib helpers (cards, step cells, WHY boxes, before/after score panels, banners, PNG+JPG export) — import it rather than rewriting them.

## Step 11 — Render, inspect, fix, repeat

1. Render the image.
2. **Look at the actual image** — open the PNG and zoom into each card (crop it if needed). Code that "should" fit often doesn't; overlaps and clipped text are only visible in the render.
3. Go through `references/checklist.md` card by card, as a junior engineer seeing it cold.
4. Fix, re-render, re-check. Do not show the user a slide that fails the checklist.

## Step 12 — Variants and final check

- **Detailed version** for technical readers (all numbers). Offer a **simple version** for a wide audience: same story, fewer exact numbers.
- Export a JPG copy (no transparency) for LinkedIn/X.
- Verify every external claim or citation that appears on the slide or in a companion post before publishing; flag any you could not verify.
- Deliver: the PNG (+ JPG), the drawing script or HTML source, and the fact sheet. Mention that `linkedin-arabic-science-post`, `tweet-post` or `figure-animator` can produce a post or an animated version from the finished slide.
