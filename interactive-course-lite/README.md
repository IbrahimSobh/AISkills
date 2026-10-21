# interactive-course-lite

Turns a table of contents, notes or docs into a free, self-paced, interactive course: one `index.html` file that works offline, where every lesson pairs a plain explanation with a live demo and highlighted code, followed by a quiz. The course ends with a final quiz and a free certificate. It plans the course with you step by step, builds it from the included template, and checks it for quality and clarity. For teachers, trainers and anyone who wants to turn material into something learners can see working.

## When to use it
- You have a table of contents, notes or docs and want an interactive course from them.
- You want each idea shown as a demo the learner drives, not only as text.
- You want to add lessons to a course built with this skill.

## Example request
> Make an interactive course from these notes on sorting algorithms.

## Example output
A folder with one `index.html` that you open in any browser, offline:
- a welcome page with the course map and what you'll learn,
- one lesson per topic: explanation, everyday analogy, a demo with Run and Step buttons beside the code it runs, and a 3-question quiz,
- a glossary or cheat sheet,
- a final quiz and a certificate with the learner's name (80% to pass; print, PDF or PNG).

Before building, the skill stops for your approval of the level and audience, the lessons, and the demo plan. After building, it runs automated tests, takes screenshots in light, dark and phone width, and reviews the text against a clarity checklist.

## Requirements
- Node.js 22 or newer
- Google Chrome or Microsoft Edge (used by the test and screenshot scripts)
- Python 3 with Pillow (`pip install pillow`): draws the small icon shown in the browser tab; the tests expect it

## Install
**Claude Code:**
```bash
cp -r interactive-course-lite ~/.claude/skills/
```
**claude.ai:** zip the `interactive-course-lite` folder, open **Customize → Skills** (claude.ai/customize/skills), choose **+ Add**, and upload the zip.

Full instructions for the agent: [SKILL.md](SKILL.md)
