---
name: "interactive-course-lite"
description: Turn a table of contents, topic list, notes or docs into a free, self-paced, interactive single-file HTML course - lessons with live demos beside highlighted code, formula strips, lesson quizzes, a glossary or cheat sheet, a final quiz and a free certificate - planned with the user step by step and checked for quality and clarity. Use this whenever the user wants to create or convert material into an online course, tutorial site or interactive lessons, even if they only say "make a course from this", or wants to add lessons to such a course. Lite version - it plans, builds and checks the course; it does not publish, make slides, READMEs, videos or posts.
---

# Interactive course builder (lite)

Build a course as one self-contained `index.html` that works offline: every lesson pairs a clear explanation
with a demo the learner drives and a code panel that lights up step by step, then a lesson quiz; the course
ends with a final quiz and a free certificate. Worked examples are in `references/examples.md`.

This lite version covers four things: **plan** the course, **build** it, add the **final quiz and
certificate**, and **check quality**. Publishing, slides, README, videos and posts are not included.

The user decides; you propose. **Stop at every checkpoint** (marked ⛳), show what you propose, and wait for
their answer before going on. Use the AskUserQuestion tool when there are clear options; otherwise ask in
plain text and end your turn.

## Resources (read when you reach the step that needs them)

| File | When |
|---|---|
| `references/course-design.md` | before the outline and before writing lessons: lesson anatomy, writing rules (clarity, flow, accuracy), demo checklist and proven patterns, quiz rules, audience and learning points, flow/accuracy review |
| `references/examples.md` | at the start: worked examples, demo ideas, lessons learned |
| `references/template-guide.md` | when building: placeholders, adding lessons, DS/KIT helpers, CSS classes |
| `assets/course-template.html` | copy to `<folder>/index.html` and fill in |
| `scripts/*.mjs`, `scripts/favicon.py` | tests, screenshots, flow audit, tab icon (run with `node` / `python -I`; no npm installs) |

Scripts need Node 22+ and Chrome or Edge (Python with Pillow for the tab icon, which the tests require). Check these early and tell the user
about anything missing. Pass absolute paths to the scripts.

## 1. Plan the course

### 0. Understand the material
Read everything the user provided. If it's long, skim its structure first. Note the subject, depth, any
code, and gaps. Read `references/examples.md`.

### ⛳ 1a. Level, audience and basics
- **Level:** offer introductory (high-level, plain words, no corner cases), intermediate (more detail,
  pitfalls, trade-offs) or advanced (in-depth mechanics, edge cases); recommend one and say why.
- **Audience:** propose 3-4 audience groups and what each wants, the prerequisites, who it is *not* for,
  and how the audience shapes the course (course-design §7). Ask if the user has a specific audience.
- **Basics:** course title; folder name (`introduction-to-x` style; lower-case, hyphens); author name and
  optional link for the welcome page; provider name on the certificate; code language for the code panels
  (or pseudo-code / none); glossary or cheat sheet. Ask for the names; don't assume them.

### ⛳ 1b. Proposed modules
Derive 5-10 modules (lessons) from the material in teaching order, grouped into Parts when there are clear
stages. For each: title and one-line purpose, 3-5 main ideas, which parts of the source it uses, estimated
minutes. Also show the three "What you'll learn" points (under 17 words each), prerequisites to introduce
early, and what you left out and why. Wait for approval or edits.

### ⛳ 1c. Demo plan
For each lesson propose one interactive demo (one clear idea; what the learner clicks; what moves; what the
code panel shows; the formula strip above it and whether it is live), using the proven patterns in
course-design §5. State the notation the course will use (course-design §4). Flag weak demos and suggest
alternatives. Say whether the welcome-page colour key fits (course-design §5). Wait for approval.

## 2. Build the course
1. Create the folder; copy `assets/course-template.html` to `<folder>/index.html`; fill the welcome page and
   placeholders (template-guide §2).
2. Write each lesson following course-design §3-5 at the chosen level, one lesson at a time, checking each
   against the clarity checklist (course-design §4) as you go: lead, analogy, demo + code panel with formula
   strip, details (tables, "how to read it"), "Where it shows up", 3-question quiz.
3. Write the glossary or cheat sheet.
4. Add the browser-tab icon: `python -I scripts/favicon.py <folder>/index.html [emoji]`.

## 3. Final quiz and certificate
### ⛳ 3a. Final quiz
Draft 10-12 questions covering every lesson (course-design §6), with the correct answers spread over all
positions. Show them with the answers marked; confirm they're simple and cover every lesson.

The certificate is already in the template: it unlocks at 80% or more on the final quiz, shows the learner's
name, can show or hide the score, prints or saves as PDF, and downloads as PNG. Fill its title, topic
sentence and provider name (template-guide §7).

## 4. Check quality
1. Run `node scripts/test_course.mjs <absolute path>/index.html` until all checks pass. Fix causes, not
   symptoms.
2. Visual check with `scripts/shot.mjs`: each demo after running, light and dark (`--theme dark`), and phone
   width (`--width 390`). Look at the images; fix overlaps, cut-off text, empty or idle states.
3. ⛳ Send the user a few screenshots and the local file path to open in a browser; apply their changes and
   re-test.
4. ⛳ Flow and accuracy review (course-design §8): `flow_audit.mjs`, a newcomer reading pass, the clarity
   checklist (vague pointers, numbers without derivation, topic switches, figures with unexplained numbers,
   nothing only in the demo), fact check, consistency, quiz check. Report what you found and changed, and
   anything that needs the user's judgement. Wait for approval.

## Working rules
- Re-run `test_course.mjs` after every change.
- Keep the user's preferences from the first draft.
- Report outcomes faithfully: say what you checked (tests, screenshots) and what you didn't.
