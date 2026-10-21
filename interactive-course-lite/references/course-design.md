# Course design: how to write lessons that teach

This is what makes these courses work, plus the lessons learned
from user feedback while building them. Read it before writing the outline and again before writing lessons.

## Contents
1. Principles
2. Course level and shape
3. Lesson anatomy
4. Writing rules (clarity, flow, accuracy)
5. Interactive demos
6. Quizzes and the certificate
7. Audience and "What you'll learn"
8. Flow and accuracy review (step 4)

## 1. Principles

- **Interactive first.** Every lesson has at least one demo the learner drives, beside a code panel whose
  current line lights up. Reading alone is not enough; the learner should *see the idea happen*.
- **Clear, in order, accurate.** Explain every new term (even in a few words) the first time it appears.
  Never assume knowledge beyond the stated audience and level. Nothing "mostly true". How deep to go, and
  whether corner cases belong, depends on the course level (§2).
- **Why before how.** Start each idea with the problem it solves, then an everyday analogy, then details.
- **Simple and free.** Single self-contained HTML file, works offline, no sign-up; the certificate depends only
  on the final quiz (80% pass mark).

## 2. Course level and shape

The user picks the level at checkpoint 1a. It changes depth, examples, demos and quizzes, not the format:

| | Introductory | Intermediate | Advanced |
|---|---|---|---|
| Goal | understand the main ideas and when to use them | use it well: how it works, trade-offs, best practice | master it: internals, edge cases, performance, failure modes |
| Assumes | nothing beyond the stated audience | the basics of the topic | solid hands-on experience |
| Content | main concepts in plain words, everyday analogies; **no corner cases** | details and mechanisms, common pitfalls and how to avoid them, comparisons and "when to use what" | in-depth mechanics, tricks, edge and **corner cases**, gotchas, performance and debugging |
| Explaining terms | every term, briefly | new and advanced terms; basics only recalled in a few words | advanced terms; link basics rather than re-teaching them |
| Demos | one clear idea, guided (Run / Step) | compare approaches, tune parameters, see a pitfall happen | stress cases: break it, find the edge, measure the cost |
| Code panels | short readable sketches | realistic code with typical patterns | real-world code, including the tricky line |
| Quizzes | direct, main concepts, answerable from the text | apply the concept to a short scenario; spot the mistake | edge cases, predict-the-output, trade-off decisions; still one clearly correct answer, all answerable from the lessons |
| Study time | 15-25 min per lesson | 25-40 min | 30-50 min |

Shape (all levels):
- 5-10 lessons. Optionally a primer first (e.g. Big-O) or two Parts with a time split (e.g. an AI course: Part A
  foundations ≈20%, Part B practice ≈80%) shown as `.part` banners and in the welcome page path.
- Fixed sections: Welcome · lessons · Glossary (concept courses) or Cheat sheet (code courses) · Final quiz &
  certificate. An optional extra section such as "Choosing a structure" or a final project is fine.
- Typical size: 3 quiz questions per lesson; 10-12 final questions; ~1-1.5k lines of HTML per 10 lessons of
  content plus the shell.

## 3. Lesson anatomy (same order every lesson)

1. `h2` with the lesson number and a short subtitle in `<small>`.
2. **Lead** (`p.lead`): the main idea in 1-2 sentences, new terms in **bold** with a plain explanation.
3. **Analogy** paragraph: an everyday comparison (open-book exam for RAG, team passing a decision for a neural
   network, careful vs adventurous friend for temperature).
4. **Interactive demo + code panel** (`.grid2` → `.card` with controls/viz/status/log, beside `.code`).
5. **Details**: short `h3` subsections with tables (`table.cx`), numbered steps (`ol.ex`), callouts.
   Good recurring blocks: comparison tables ("X vs Y"), "When to use what", "In practice:" callouts with
   concrete numbers, "How to read it" notes under a demo.
6. **"Where it shows up"**: 2-4 real-world uses.
7. **Quiz** (`div.quizbox`): 3 questions.

Keep lessons proportionate: a foundations lesson ~15 minutes, a core lesson 25-30 minutes of reading + demos.

## 4. Writing rules

**Clarity**
- One idea per paragraph; short sentences; active voice; concrete examples with real numbers.
- Bold a term where it is introduced and explained, not elsewhere (the flow audit relies on this).
- Prefer a small table over a long paragraph when comparing things.
- Practical guidance where learners need it ("low temperature for facts and code, high for brainstorming";
  "chunks too big bring noise, too small lose meaning"; "use the simplest option that does the job").

**Flow (the most common fix requested)**
- Never use a term before it is explained. If a later lesson covers it properly, explain it briefly here and
  point forward: "(tokens, lesson 4)", "(more in lesson 6)".
- Acronyms: expand on first use ("large language model (LLM)").
- Jargon that the audience may not know (JSON, API, vector, parameter, system prompt) gets a short gloss on
  first use, even inside brackets.
- Each lesson's opening should connect to the previous one when it builds on it ("Same idea as lesson 2,
  bigger model").
- Name concepts the learner will meet elsewhere (e.g. "agent loop", "ReAct") in one sentence, tied to what the
  course already showed.

**Never assume: the clarity checklist** (the user's top priority; check every paragraph, table, figure,
demo label and status message against it while writing, not only at the review)

The five problems that slip through most often:
- **Vague pointers.** Words like "both", "this", "it", "they", "these", "someone", "the two…" or "the above"
  must point to something already named in the text, close by. If the reader would have to guess what is
  meant, name it instead ("permutations and combinations both…", "a person who has been picked…"). Never
  point to something that only appears later, or only inside a demo (see the last item).
- **Numbers without derivation.** Every number that is a result (a total, a probability, an average, a
  percentage, a count) shows where it comes from, in the text, at the point it appears: the inputs, the
  operation, the result ("5 × 4 × 3 = 60"; "9 ÷ 98 ≈ 9%"). If an input comes from a table, a demo or an
  earlier step, say so ("from the table above", "the demo counts 31 emails"). Prefer a small case the
  learner can check by hand ("with 4 people: AB, AC, AD, BC, BD, CD"). Rounded values that don't multiply
  back exactly get a note. The only exception is a result that needs maths beyond the course level; then
  say how it was obtained ("the demo computes this area").
- **Topic switch without a transition.** When a section moves to a new example, object or idea, the first
  sentence says so and links it to what came before: "The complement rule from the table above is most
  useful when… This example leaves the cards and uses a die."
- **Figures with unexplained numbers.** Every number, label, area, bar or line in a figure or chart is
  explained in the text or caption, twice: by the formula and by what the learner sees ("the high-sales
  piece is 0.45 out of the 0.60 sunny area, so 0.45 ÷ 0.60 = 0.75"). Explain how to read the figure before
  relying on it (what the axes, widths, colours or dashed lines mean). A figure that repeats a result
  should say how it relates to the earlier calculation (a check, or the same idea seen another way).
- **Nothing only in the demo** (the most common gap in course reviews). The text must
  stand on its own for a reader who doesn't run the demo, or reads on a phone:
  - Before each demo, say what every mode, button, task or option does, and what to watch for
    ("Run RAG shows the four steps; Ask without RAG shows the model guessing without the handbook").
  - Every result the text mentions (a number, a winner, "the best of the three questions") is worked
    out in the text, with all its inputs, even if the demo also shows it. If the text says "three", name
    all three.
  - No pointers into a demo's steps ("as step 4 showed", "the last steps of demo 2"): restate the fact
    itself ("knowing heads leaves 3 even cells out of 6, so P(even | heads) = 1/2").
  - Jargon that appears only in the demo (a query, a code name, a formula on a status line) is explained
    in the text too.

Also check:
- Everyday objects and settings used in examples (a die, a card deck, spam, a sports league) get one plain
  sentence of explanation the first time; prefer examples that work in any culture (handshakes, PINs,
  meals) over local ones (a particular lottery, a currency).
- Counts in the text match what follows ("three rules" before a three-row table).
- Made-up demo data must not suggest something false about the real world: if a slider can produce an
  unrealistic pattern, say it's only there to show the pattern.

**Notation** (decide once, at checkpoint 1c, and use it everywhere)
- Write maths as maths in everything the learner reads: subscripts and superscripts (log₂, 2³, 2⁻¹), Σ, ≈, −
  (minus sign, not hyphen). Code panels keep the language's names (`math.log2`); say once where they meet
  ("in Python, log₂(n) is `math.log2(n)`").
- Use the field's standard forms when the course leads into that field (for AI/ML: −log p, H(p, q),
  KL(p‖q), lowercase p and q for distributions, NLL, logprobs). Show the friendlier equivalent once, where the
  idea is introduced (−log₂ p = log₂(1/p)), then stick to the standard form.
- One unit and one base across the course; mention other units once where learners will meet them (bits vs nats).

**Accuracy**
- Introductory: state what is true for the general case; drop corner cases rather than over-qualify.
  Intermediate/advanced: cover the important exceptions explicitly, with an example of each.
- If a demo simplifies (hand-set weights, toy model, 3-dimensional embeddings), say so on the page.
- Fast-moving facts (dates, product names, model sizes, prices): verify with a current source or phrase them
  so they stay true ("billions of parameters", "introduced in 2017").
- Numbers shown in demos must be consistent (if a sum is shown, the displayed total must match it).

## 5. Interactive demos

The demo is the heart of each lesson. Propose one idea per lesson at checkpoint 1c and get approval.

**Good demo checklist**
- Shows exactly one idea; the learner controls it (Run, Step, Reset, sliders, toggles, choice buttons).
- Code panel beside it highlights the line being executed (`cp.hl(n)`); status line says what just happened
  in plain words; optional log keeps a history.
- Names every colour that carries meaning in the demo's own words (caption, status line or lesson text), e.g.
  "orange = spam", "green dashed line = the average". Learners should never need a key from another page.
- **Shows its formula** (formula-first figures): the learner should always see the rule that produces the
  numbers, next to the numbers.
  - A **formula strip** (`.fstrip`) sits just above every figure that computes something: the formula the
    figure shows, e.g. `H = −Σ p log₂ p`, `I(X;Y) = H(X) + H(Y) − H(X,Y)`. Same place and look in every lesson.
  - Make it **live** when a control changes the result: substitute the current values, e.g.
    `2³ = 8 ⇔ log₂(8) = 3` following a slider, or `P(bit wrong) = 3p²(1−p) + p³ = 2.8%` following the noise.
    Step-through demos fill in the current term and the running sum under the formula
    (`−0.50 × log₂ 0.05 = 2.161`, `sum: 0.032 + 1.095 + 2.161 = 3.288`).
  - **Tables:** put the formula in the column header (e.g. "surprise" with `−log₂ p` under it), keep plain
    numbers in the cells. A full expression in every cell wraps and becomes hard to scan, especially on phones.
  - **Inside the figure:** axis titles, meter labels and legends name the quantity by its formula
    (`y = log₂(x)`, `loss = −log₂ q`). When parts of a formula play different roles, colour them and reuse the
    same colours in the figure (e.g. yellow = weight, purple = surprise, with matching tags on the bars).
  - **Clarify, don't crowd:** one formula idea per figure. If a figure needs a legend longer than its
    caption, split it or drop it (a single waterfall of signed terms read better than a per-event split panel).
  - Formula text inside upper-case captions keeps its case: wrap it in `<span class="nt">…</span>`.
- Colour key (welcome page) only if it fits: when most demos show items moving through the shared `.node` states
  (`.node` normal, `.active` in use now, `.visited` already seen or kept, `.found` result), as in data-structure
  or AI courses, keep the key, use the states consistently, and rewrite its four lines for the subject. When demos are
  mostly charts, plots, cards or dots whose colours mean different things per demo (as in a probability course), delete
  the key and its CSS. State the choice in the demo plan (checkpoint 1c).
- Never idles: no fixed number of rounds that do nothing visible; stop when converged and say so.
- Smooth: animate state changes (one item at a time, glide positions), respect `DS.wait()` so the speed slider
  works, and run inside `DS.run(root, fn)` so buttons disable while busy.
- Deterministic and realistic data (seeded `KIT.rng`); data noisy enough that errors are visible.
- Only meaningful interactions are clickable; no placeholder/generic results presented as real.
- Readable in light and dark mode and at 390px width; text in SVG uses `var(--text)` etc.
- Default state is already informative (render the initial picture, not an empty box).

**Proven demo patterns** (see examples.md)
| Pattern | Examples |
|---|---|
| Step-through of an algorithm on boxes | stack push/pop, queue, linked-list append with a moving pointer, BST insert/search, hash buckets |
| Memory/state boxes with types | Python variables, function call frames (local vs global names) |
| Plot + fitted model + error meter | house-price line fit with live parameters, polynomial over/underfitting with train/test error |
| Network diagram whose edges change | 2-3-1 neural network learning XOR |
| Choose a mode / variant and compare | supervised vs unsupervised vs reinforcement; 2 vs 3 clusters; "too tired" vs "too wide" attention |
| Chips / tokens / bars | tokenizer chips with a context-window meter; next-token probability bars with a temperature slider |
| Toggle ingredients, see the effect | prompt builder with a quality checklist; defences against prompt injection |
| Pipeline with numbered stages | RAG: embed → search → top-k → augmented prompt → answer |
| Loop diagram + chat transcript | agent think → act → observe with memory chips and a context meter |
| Formula-first step-through | live formula strip above two aligned bar charts (p above q); Step adds one term to a table, a running-total bar and the strip; "Show both" compares H(p, q) and H(q, p) |
| Waterfall of signed terms | each term moves a running total right (+) or left (−) from a dashed zero line; total row at the end (KL divergence terms) |
| Curve with labelled cases | event cards as dots on y = −log₂ p; clicking a card highlights its dot and fills a meter and the strip |
| Interactive tool | type explorer, expression evaluator, string slicer, traceback reader, quiz game project |

## 6. Quizzes and the certificate

- Lesson quiz: 3 questions on that lesson's main ideas; final quiz: 10-12 questions covering every lesson.
- One clearly correct answer, three plausible wrong ones, a one-sentence "why". Every question must be
  answerable from the lesson text; never test something the course didn't teach.
- Difficulty follows the level (§2): introductory = direct questions on main concepts, no tricks or corner
  cases; intermediate = short scenarios and spotting mistakes; advanced = edge cases and predict-the-output
  (which the lessons must have covered).
- Spread the correct index across positions; avoid "all of the above".
- Pass mark 80% (`needed = ceil(0.8 × N)`). The certificate depends only on the final quiz. The learner can
  show or hide the score, print/save as PDF, or download a PNG; after passing, an optional line invites them to star the course's repo (only if it has one).
- Certificate body: "has completed the self-paced course and passed its final quiz, covering …" with a
  one-sentence topic list.

## 7. Audience and "What you'll learn"

- **What you'll learn**: exactly 3 points, each under 17 words, outcome-focused, shown on the welcome page. Pattern: (1) the foundations/how it works, (2) how to use/apply it, (3) limits, choices or
  judgement. Pick an emoji per point for the welcome page.
- **Main audience**: one sentence with the level and prerequisites, 3-4 bold groups with what each gets,
  then one sentence on who it is *not* for. Examples:
  - Python: complete beginners, students, professionals automating tasks, programmers from another language;
    not for experienced Python developers or advanced topics.
  - Data structures: programmers who know the basics (CS students, self-taught/bootcamp developers, interview
    prep, junior developers); not for advanced structures or formal proofs.
  - AI: beginners using AI at work, decision makers, students/career changers, developers new to AI; not for
    ML engineers wanting maths or training code.

**How the audience shapes the course** (decide this at checkpoint 1a, then apply it everywhere):

| Audience | Examples and analogies | Code panels | Demos | Tone |
|---|---|---|---|---|
| Non-technical professionals | workplace and everyday situations (emails, reports, customers) | short readable sketches, clearly optional | guided Run/Step, choose-and-compare | plain words, no jargon without a gloss |
| Managers and decision makers | business cases, costs, risks, "when to use what" | minimal | comparisons and trade-off tools | outcome-focused, practical guidance tables |
| Students | textbook-style examples, exam-relevant definitions | real code, line by line | step-throughs of each operation | precise definitions, consistent terms |
| Developers | realistic tasks, production pitfalls | real, idiomatic code | tune parameters, break it, inspect state | direct, technical, assumes tooling |

Mixed audiences: write for the least experienced group named, and add short "in practice" callouts for the
more experienced ones.

## 8. Flow and accuracy review (step 4)

Run after the course passes `test_course.mjs`, before handing the course over.
1. `node scripts/flow_audit.mjs <index.html>`: lists bold terms used before the lesson that explains them.
   Treat it as a starting list (it has false alarms); fix real ones by a brief explanation or a forward pointer.
2. Read `flow_text.json` lesson by lesson as a newcomer: any term, acronym or step that isn't explained yet?
   Does each lesson build on the previous? Then delete `flow_text.json` (it is written next to the course).
3. Clarity pass: read every lesson again, including tables, figure labels and captions, demo buttons and
   status messages (in the `<script>` blocks) and quiz explanations, and check each item of the clarity
   checklist (§4). Look hardest for vague pointers, numbers without derivation, topic switches without a
   transition, figures with unexplained numbers and anything that exists only in a demo. For the last one,
   search the lesson text for "step", "demo", "mode", "button", "three", "the best of" and "above"/"below",
   and compare each demo's options, tasks and data arrays in its `<script>` with what the text says.
   `flow_text.json` leaves out figure captions, card status lines and demo text, so check the page itself
   before reporting something as missing. For a large course, write the findings as a table per
   lesson (location, problem, suggested fix) and show it to the user before fixing.
4. Accuracy pass: list the factual claims (numbers, dates, names, "X does Y"); check anything uncertain or
   fast-moving against a reliable source; soften or remove what can't be confirmed.
5. Consistency: same names in lessons, glossary, quizzes, and course map. If the welcome page has a
   colour key, check that the demos really use those `.node` states and that its wording fits the subject;
   if not, remove or rewrite it. Check each demo names its meaningful colours (§5). Check every computing
   figure has its formula strip, table headers carry their formulas, and the notation is the same in text,
   strips, tables, figure labels, quizzes and glossary (§4 Notation, §5).
6. Quiz pass: each question answerable from the text; exactly one correct option.
7. Show the user a short report: what was found, what was changed, anything left for their judgement.
