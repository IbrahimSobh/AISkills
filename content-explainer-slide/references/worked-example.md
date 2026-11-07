# Worked example: "36 idle neurons got a job" (MNIST neuron surgery)

The slide this skill was distilled from. Use it to calibrate what "clear enough" looks like — not as a template to copy literally.

**Input:** a small MNIST digit classifier (a CNN with one 128-neuron hidden layer), saved models before/after a hand edit, and result logs. Data mode → matplotlib PNG, numbers computed from the saved models at render time.

**Fact sheet highlights:** 36 of 128 hidden neurons never fire (measured on 18,000 labelled training images — an earlier version measured on 3,000 and got 38, which contradicted the draft post; fixed by computing it once from one sample). Test accuracy 96.74% → 96.99% on 10,000 never-used test images (34 fixed, 9 broken). Referee check on 21,000 other unused images: 88 fixed vs. 37 broken (~6 in a million by luck).

**Headline:** "36 of my network's 128 neurons were doing nothing. So they got a job."

## Card 1 — Discovery: "Which neurons are idle?"
- Takeaway: 36 of 128 neurons are active on 0% of images.
- Figure: histogram of the 128 neurons sorted busiest → idle; idle in red, active in grey (legend).
- Data label: "18,000 of 60,000 training images (30%) — used to build the fix; the rest stay unseen so the final check is fair."

## Card 2 — Problem: "Which digits does the network confuse?"
- Problem A: '3' acts as a magnet — it takes 139 wrong predictions from other digits → fixed by Set A.
- Problem B: 7 and 8 are the weakest digits (94.7%, 94.8%) → fixed by Set B.
- Exclusion with reason: 9 is not targeted, because most lost 9s are predicted '7', and lowering '7' would hurt the 7s being rescued.

## Card 3 — Method: "How does one idle neuron become a mistake detector?" (2×2 cells)
1. WHAT: Collect examples of one mistake — true 8s predicted as '3'. Picture: six real thumbnails + "… 21 in total".
2. WHAT: Pattern = average of these 8s − average of real 3s. Picture: the real difference image, legend "red = only in these 8s, blue = only in real 3s". WHY: the network scores both as '3'; subtracting real 3s removes what they share and keeps only what marks an 8, so it won't fire on real 3s.
3. WHAT: Compare a NEW 8 (never seen) with the pattern from step 2. Picture: new 8 "vs" pattern → "strong match → the neuron FIRES". WHY: the firing bar is set so almost no real 3 passes.
4. WHAT: Wire the neuron ONLY to '3', with a negative weight. Picture: before scores "predicts 3 ✗" → after "predicts 8 ✓", note "8, the 2nd-highest, wins". WHY: it can only LOWER '3' — if another digit already has the top score, nothing changes, so other predictions are untouched.
- Footnote: pictures show pixels; the real comparison uses the network's internal features. "Same recipe for all 30 detectors."

## Card 4 — Counts: "Where do the 30 detectors come from?"
- Each mistake's examples are split into handwriting styles (k-means); one style → one detector. Example box: "21 examples of 8→'3' → 3 styles → 3 detectors", each style boxed with its averaged thumbnail.
- Rules: a style needs ≥2 images; a mistake with <3 examples is skipped as too few to learn.
- Set A (fake-3 detectors) = 11; Set B (stolen-7/8 detectors) = 19, built partly from 2,897 mined suspect images (light bars vs. dark bars for labelled, with legend). "×N = N style detectors for that mistake."
- Total chain: 11 + 19 = 30 of 36 idle neurons; 6 spare.

## Card 5 — Result: "Did it work on new images?"
- Test (10,000 never used): 96.74% → 96.99%, 34 fixed, 9 broken. Digit 8: 94.8% → 95.9%; digit 7: 94.7% → 95.6%.
- Referee (21,000 other unused): 88 fixed vs. 37 broken — about 6 in a million by luck.
- Chart: correct predictions per digit, after − before (green +, red −, grey 0).
- "Why each digit changed": 7 and 8 rescued by both sets; 2, 5, 1 gave a little back to fake-3 detectors; 4 gained because lowering '9' let 4 win; 3 and 9 lost a few because their scores were lowered.
- Conclusion banner: idle neurons can be turned into mistake detectors by hand, without training — a small but real gain that holds on new images.
- Lesson banner: hand-editing weights removes obstacles well; teaching a genuinely new skill still needs training.

## Review feedback that shaped it (what went wrong in early versions)
- "Where did these numbers come from?" → number chains, data labels.
- "All 30 detectors? Not 36? How?" → totals with leftovers explained.
- "What is Set A?" → names defined where first used, problem ↔ fix pairing.
- "Why subtract real 3s? Why are other digits untouched?" asked several times → WHY boxes inside each step, never in footnotes.
- Empty right half of card 5 → chart widened, explanation panel moved into the space.
- Style groups blurred together → each group in its own box.
