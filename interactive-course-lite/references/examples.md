# Worked examples and lessons learned

Use these as references for course shape, tone, depth and demos. They are sketches of good courses on three
topics, not files you can open.

## Course shapes that work

| Topic | Shape | Final quiz |
|---|---|---|
| Data structures | a short primer (Big-O) + 5 lessons + a "choosing a structure" lesson + a complexity cheat sheet | 10 (pass 8) |
| Python for beginners | 10 lessons including getting started and a final quiz-game project + a cheat sheet | 10 (pass 8) |
| Introduction to AI | Part A (3 short foundation lessons, ≈20% of the time) + Part B (7 lessons, ≈80%) + glossary | 12 (pass 10) |

## Demo ideas that worked

**Data structures:** every operation animated on boxes and pointers, with the exact line of a real method
highlighted; figures show the shape (nodes, pointers, buckets); a "choosing a structure" comparison; quiz
questions on main operations and their costs only.

**Python:** memory boxes labelled with types show what each line does; local vs global names appear as a
separate box during a function call; hands-on tools (type explorer, expression evaluator, string slicer,
collections playground, module explorer, traceback reader); a playable final project.

**AI:** one demo per idea, from a perceptron line and k-means (choose 2 or 3 groups) to an agent loop; models
explained as formulas with parameters, from `y = a·x + b` up to LLMs; object detection showing classification
(label) and regression (box) together; attention explained step by step with clickable examples; practical
guidance tables (temperature, chat vs RAG vs agent, prompting vs RAG vs fine-tuning).

## "What you'll learn" examples (3 points, < 17 words)

- AI: How machines learn from data, from a simple line to neural networks and LLMs. · How to use generative
  AI well: prompting, context engineering, RAG, agents, MCP and fine-tuning. · When AI can be wrong, its main
  risks, and when a person must check it.
- Data structures: How stacks, queues, linked lists, binary search trees and hash tables work inside. · How fast
  each operation is, using Big-O, and how to choose the right structure. · How each structure maps to real
  Python code, line by line, with animations.
- Python: Python basics: variables, data types, operators, strings, and decisions and loops. · How to organise
  code with lists, dictionaries, functions and modules, and handle errors. · How to write and debug small
  programs of your own, ending with a quiz-game project.

## Lessons learned (apply from the start)

- Keep it simple: a page to read, understand, take the quiz and get a nice certificate. No accounts.
- Quizzes for introductory courses: direct, main concepts only, answerable from the text; certificate = final
  quiz only (80%). For intermediate/advanced courses follow the level table in course-design §2.
- Explain terms before using them; add brief explanations and forward pointers; review the whole flow at the end.
- Demos: realistic (scattered data, visible errors), smooth (no idle rounds, no sudden jumps), meaningful
  interactions only, practical "when to use what" guidance next to theory.
- Formula-first figures: every computing demo shows its formula in a strip above the figure (live when values
  change); table headers carry the formula, cells keep plain numbers; formulas must clarify, not crowd. Show a
  mockup image before large visual changes.
- Notation: proper maths (log₂, superscripts) outside code; use the target field's standard forms (for ML:
  −log p, H(p, q), NLL) and show the friendlier form once.
