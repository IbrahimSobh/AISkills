# Using assets/course-template.html

The template is a complete course shell with every course-specific part replaced
by `{{PLACEHOLDERS}}` and one generic example lesson. It already runs: open it in a browser, or run
`node scripts/test_course.mjs assets/course-template.html` (only the placeholder check fails).

## Contents
1. File map
2. Placeholders
3. Adding lessons
4. JavaScript helpers (DS, KIT)
5. CSS building blocks
6. Glossary or cheat sheet
7. Final quiz and certificate
8. Things to keep

## 1. File map (top to bottom)

| Part | What it is | Edit? |
|---|---|---|
| `<head>` theme script + big `<style>` | colours (light/dark), layout, nodes, code panel, quiz, callouts, tables | rarely (add lesson CSS inside the lesson's own `<style>`) |
| `<header class="top">` | brand, animation speed slider, theme button | brand text only |
| `DS` script | shared helpers (below) | no |
| demo CSS + `KIT` script | plots, meters, chips, flows, chat, part banners, seeded RNG | no (add helpers if needed) |
| `#intro` section | welcome page | yes: all placeholders |
| `#lesson1` section + script | example lesson and demo | copy per lesson, replace content |
| `#glossary` section + script | glossary/cheat sheet table with topic filters | rows + title |
| `#finalquiz` section + script | final quiz, certificate, print, PNG download | questions, title, topics, repo, provider |
| `<footer>` + nav script | footer links; sidebar built from `section[data-title]` | footer text |

## 2. Placeholders

Search for `{{` and replace all of them; `test_course.mjs` fails while any remain. Main ones:
`COURSE_TITLE`, `BRAND_EMOJI` (also becomes the tab icon via `scripts/favicon.py`, so pick one that reads at 32 px), `BRAND_SHORT` (e.g. "Intro to AI"), `INTRO_LEAD`, `EMOJI_1..3` +
`LEARN_POINT_1..3`, `THEORY_PILLAR`, `PRACTICE_PILLAR`, `N_LESSONS`, `N_LESSON_QS`, `N_FINAL_QS`,
`PASS_COUNT` (= ceil(0.8 × N_FINAL_QS)), `PREREQUISITES`, path steps, `TIP`, course map links,
`LESSON_n_TITLE`, `GLOSSARY_TITLE`, `CERT_TOPICS`, `GITHUB_USER`, `REPO_NAME`, `PROVIDER_NAME`, `AUTHOR_NAME` and `AUTHOR_URL` (the small italic "By …" byline
under the welcome title,; ask the user for both; for example a name and
a profile URL; the name is the link text, never the URL).
The colour key on the welcome page (`KEY_*` placeholders, between `<!-- COLOUR KEY -->` comments) is optional:
fill it in for the subject if most demos use the `.node` states, otherwise delete the block and the `#intro .ckey`
CSS rules (decided at checkpoint 1c, course-design §5).
Placeholders inside JS strings (`"{{COURSE_TITLE}}"`) appear twice in the certificate code (screen and PNG):
replace both.

## 3. Adding lessons

For each lesson, copy the whole `<!-- === 1 -->` block: the `<section>` **and** the `<script>` after it.
- Give the section a short unique `id` (used in links, the course map, glossary rows and anchors) and
  `data-title="N. Title"` (the sidebar is built from `data-title`; part banners have none and are skipped).
- Scope every selector to the lesson: `document.querySelector("#rag .w-rag")`, class names prefixed per demo
  (`.rg-go`, `.rg-q`) so two demos never collide.
- Wrap each lesson script in `(() => { … })();`.
- Course map: one `<a href="#id">Title<small>3-6 words</small></a>` per lesson, in order.

## 4. JavaScript helpers

`DS` (always available):
| Helper | Use |
|---|---|
| `DS.el(tag, props, ...children)` | create elements; props: `class`, `style` object, `dataset`, `html`, `onclick`, attributes |
| `DS.svg(tag, attrs, ...children)` | SVG elements |
| `DS.code(container, src, title)` → `{ hl, clear, lines }` | code panel with Python-style highlighting; `hl(3)`, `hl(3, 4)`, `hl("text")`, `hl({ find, after })` highlights lines and scrolls to them |
| `DS.run(root, asyncFn)` | runs a demo; disables `root`'s buttons (except `.always`) and sets `root.dataset.busy` while running; ignores clicks while busy |
| `DS.wait(mult)` | pause 650 ms × mult ÷ speed slider; use between visible steps |
| `DS.sleep(ms)` | fixed pause (not scaled) |
| `DS.log(logEl, html, kind)` | prepend a log line; kind `"ok"`, `"err"`, `"info"`, `""` |
| `DS.quiz(container, questions, onChange?)` | quiz; questions `{ q, options, answer, why }` (q and why may contain HTML) |
| `DS.randInt(a, b)`, `DS.parseVals(str)`, `DS.esc(str)`, `DS.reducedMotion()` | small utilities |
| `DS.speed` | current speed (tests set it to 40) |

`KIT` (demo helpers):
| Helper | Use |
|---|---|
| `KIT.rng(seed)` | seeded random generator → same data every load |
| `KIT.gauss(r)` | roughly normal noise (std ≈ 0.29; multiply for spread) |
| `KIT.plot(container, { w, h, x0, x1, y0, y1, xl, yl, xt, yt, pad })` → `{ svg, X, Y, g }` | axes + grid; draw into `g` with `X(x)`, `Y(y)`; point classes `pt a|b|c|u|test|bad`, line class `fit` |
| `KIT.softmax(logits, T)`, `KIT.cosine(a, b)` | probabilities with temperature; vector similarity |

Busy contract: anything animated must run via `DS.run`, so tests can wait for
`[data-busy]` to clear. Buttons that must stay usable during a run get class `always`.

## 5. CSS building blocks

- Layout: `.grid2` (demo card + code, stacks under 1050px), `.card`, `.controls` (+ `.sep`), `.viz` (+ `.caption`),
  `.status`, `.log`, `.code`.
- Text: `.lead`, `.callout` (`.tip` green, `.warn` orange), `table.cx`, `ol.ex` numbered steps, `.order` link grid.
- States (the optional colour key): `.node`, `.node.active`, `.node.visited`, `.node.found`, `.node.removed`, `.node.dim`, `.node.new`.
- Formulas: `.fstrip` (formula strip above a figure; one `<span>` per formula, wraps per span on phones),
  `.formula` (larger formula box in the lesson text, `<small>` for its one-line reading), `.nt` (keeps the case
  of formula text inside upper-case `.caption` / `.sub-cap`).
- Demo extras: `.meter > .bar > i(.hot|.ok|.violet)`, `.toks > .tk`, `.cand` probability bars, `.flow` stage
  boxes (`.node` + `.arr`), `.chat > .m.(user|think|act|obs|ans)`, `.answerbox`, `.toggles`, `.mini-table`, `.part`.
- Colours: use variables, never hex: `--accent`, `--hot`, `--ok`, `--violet`, `--bad`, `--s1…--s5`, `--text`,
  `--text-2`, `--muted`, `--surface`, `--surface-2`, `--border`. Both themes then work automatically.
- Buttons: default = primary; `.secondary` = outlined; `aria-pressed="true"` for selected mode buttons (add a
  lesson-scoped style like `#whatis [aria-pressed="true"] {…}`).

## 6. Glossary or cheat sheet

Rows are `[topic, "#lessonId", term, meaning]`; topics become filter buttons. Concept courses use a glossary
(30-40 terms); code courses can turn this section into a cheat sheet .

## 7. Final quiz and certificate

- `finalQs`: 10-12 questions (see course-design.md §6). `PASS = 0.8`; `needed` and the welcome-page numbers
  must agree.
- Certificate: title, `CERT_TOPICS` sentence, `PROVIDER` (the course author, fixed, never learner input),
  `REPO` (optional star link: if the course has no GitHub repo, remove the star line and leave `GITHUB_USER`/`REPO_NAME` unused). The PNG download draws the same certificate on a canvas (white background).

## 8. Things to keep

Theme persistence key, speed slider, the "Tip" callout, colour key, footer star link, `rel="noopener"` links,
no external scripts/fonts/CDNs (the course must work offline), mobile layout (sidebar becomes a chip bar).
