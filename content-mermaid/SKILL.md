---
name: content-mermaid
description: Create and style Mermaid diagrams (flowcharts, sequence diagrams, state diagrams, ER diagrams, class diagrams, Gantt charts, mindmaps, timelines) for technical processes, workflows, architectures, and system flows. Use whenever Ibrahim asks for a "mermaid diagram," "flowchart," "sequence diagram," "state machine," or wants to visualize a software/technical process (agile workflow, CI/CD pipeline, git workflow, data model, architecture, API flow) as a diagram meant to render natively in a Mermaid-aware surface — chat canvas, GitHub/GitLab README, Notion, Obsidian, docs sites. Also trigger to fix, restyle, recolor, or improve readability of an existing Mermaid diagram. Mermaid computes node sizing, arrow routing, and text wrapping itself, so this skips content-diagrams' hand-coded-SVG verification (render-crop-check, cairosvg, manual geometry). If the deliverable must be a standalone image file for a platform that can't render Mermaid (LinkedIn/X post, raster cover), use content-diagrams instead.
---

# Content Mermaid

Produces Mermaid diagrams for technical processes and structures. This is the fast, syntax-driven counterpart to `content-diagrams`: same visual-clarity standards, but built on a language that already guarantees correct geometry, so the effort goes into picking the right diagram type and a readable, consistent color system instead of verifying coordinates.

## Relationship to content-diagrams

Both skills share the same standards — legible text, a real color system instead of decoration, clarity over density — but content-diagrams computes its own SVG geometry by hand while this skill hands geometry entirely to Mermaid's layout engine; pick between them based on where the diagram will actually be viewed (native Mermaid surface vs. a platform that only shows static images), not habit, and if genuinely unsure, ask — Mermaid source doesn't screenshot cleanly into a polished standalone graphic without real rework.

## Why there's no verification loop here

`content-diagrams` spends most of its effort on geometry: an SVG line, box, or label is just numbers Claude computed, and computed numbers can be wrong — hence render, screenshot, crop, and check.

Mermaid removes that failure mode entirely. Node width, text wrapping, arrow paths, and collision avoidance between elements are the *renderer's* job, not Claude's — the renderer will not place a label on top of a box or route a line through a shape. Re-deriving that verification loop here (screenshotting the rendered diagram, cropping, checking overlaps) would just burn tokens and latency confirming something the tool already guarantees.

What can still go wrong is entirely different, and entirely textual:
- Broken syntax (unclosed brackets, a reserved word used as a node ID, mismatched arrow types)
- An edge referencing a node ID that's never defined
- Poor color contrast (a fill and text color that don't actually read against each other)
- The wrong diagram type for the content's actual structure

So verification here means: read the syntax once for correctness, check every classDef pairs a fill with a genuinely contrasting text color, and confirm the diagram type matches what's being modeled. No image rendering required.

## Diagram type selection

Pick the type from what the content structurally *is* — this is the Mermaid equivalent of content-diagrams' motif selection:

| Content structure | Mermaid type |
|---|---|
| Sequential steps with branches/loops (a process, a workflow, an algorithm) | `flowchart TD` (top-down) or `LR` (left-right for pipelines/timelines) |
| Time-ordered messages between actors/services (API calls, protocol exchanges) | `sequenceDiagram` |
| An entity's states and the transitions between them (a lifecycle, a state machine) | `stateDiagram-v2` |
| Data model / entity relationships (schemas, DB tables) | `erDiagram` |
| Object-oriented structure (classes, inheritance, interfaces) | `classDiagram` |
| Schedule with durations and dependencies | `gantt` |
| Hierarchical breakdown / brainstorm with no strict sequence | `mindmap` |
| Chronological narrative (history of a project, version history) | `timeline` |
| Two-axis prioritization (impact vs. effort, etc.) | `quadrantChart` |

Don't default to `flowchart` for everything — a request like "diagram how our services call each other" is a `sequenceDiagram` even though it's tempting to draw it as boxes and arrows; a request like "show the states a ticket goes through" is `stateDiagram-v2`, not a flowchart with diamonds standing in for states.

## Color and readability system

This is the one place manual verification still matters, because Mermaid will happily render illegible color choices without complaint.

**The rule: every `classDef` must pair a fill with a text color that's been deliberately chosen to contrast with it — never leave `color` unset and hope the theme's default works.** Mermaid's own default palette (soft green/pink/blue with black text) is fine precisely because fill and text were chosen together; the moment you override `fill` to something more saturated or dark, you must also set `color` explicitly, or you'll reproduce the exact defect Ibrahim flagged: readable-looking boxes with text that's actually low-contrast against them.

Two palette recipes, pick one and use it consistently across every class in one diagram (don't mix):

1. **Dark fill / white text** (the default — proven, high contrast, reads well in both light and dark chat themes):
   ```
   classDef category1 fill:#1e3a5f,stroke:#0d1f33,stroke-width:2px,color:#ffffff
   ```
2. **Light tint fill / dark text / saturated stroke** (use when a diagram needs to sit visually next to a content-diagrams SVG that follows its light-tint convention):
   ```
   classDef category1 fill:#e1f0ff,stroke:#1e3a5f,stroke-width:2px,color:#1a1a1a
   ```

Borrowing content-diagrams' rule directly: **one hue per category, applied everywhere that category shows up** — the same color in fill/stroke on every node of that role, not a one-off. Assign hues by role, e.g.:
- Blue → inputs / data / backlog items
- Green → process / active work steps
- Amber or brown → decision points / gates
- Purple → outputs / releases / terminal states
- Red → feedback loops / failure paths / retrospective

**Lock the canvas so it doesn't depend on the host's light/dark mode.** Put an init directive as the very first line of the diagram:
```
%%{init: {'theme': 'base', 'themeVariables': { 'fontFamily': 'Trebuchet MS, Verdana, Arial, sans-serif', 'fontSize': '16px', 'primaryColor': '#1e3a5f', 'primaryTextColor': '#ffffff', 'primaryBorderColor': '#0d1f33', 'lineColor': '#666666', 'background': '#ffffff' } } }%%
```
`theme: 'base'` plus explicit `themeVariables` means the diagram looks the same regardless of which Mermaid theme the host environment defaults to — don't rely on the default theme name (`default`, `dark`, `forest`, etc.) alone, since that leaves the actual colors up to whatever the renderer decides.

**Font size**: 16px minimum for any diagram with more than a handful of nodes; 14px only if the diagram is simple enough that legibility isn't in question. If a diagram needs to shrink below 14px to fit its labels, that's the same "clarity over density" signal from content-diagrams — split the diagram or cut content, don't shrink text further.

**Styling reach differs by diagram type**: `flowchart`, `stateDiagram-v2`, and `classDiagram` all support per-node `classDef`/`class` assignment directly, so use the category-color system above node by node. `sequenceDiagram`, `erDiagram`, and `gantt` have much more limited per-element styling — for those, put the effort into the `themeVariables` in the init block (`actorBkg`, `actorTextColor`, `noteBkgColor`, etc. for sequence diagrams) rather than expecting node-level classes to work the same way.

## Arrow grammar

Unlike hand-coded SVG, Mermaid renders arrow labels cleanly with automatic placement — `-->|label|` text doesn't risk landing on top of a shape the way a manually-positioned SVG label would. So, unlike content-diagrams' "keep text off arrows, decode via legend" default, **labeling arrows directly is fine and often clearer** here. Still keep labels to short fragments ("approved," "retry," "on failure") rather than phrases — a label is a tag, not a sentence.

Reserve line *style* for the same broad distinction content-diagrams uses:
- Solid arrow (`-->`) → primary/normal flow
- Dashed arrow (`-.->`) → feedback, an optional path, or an external/indirect interaction
- Thick arrow (`==>`) → an emphasized or critical path, used sparingly

## Keep labels short; use subgraphs to group

Node text should be a short phrase, not a sentence — Mermaid will wrap or overflow awkwardly on paragraph-length labels just like any other tool. If a node needs multiple lines, insert them explicitly with `<br/>` inside the label rather than trusting auto-wrap to break in a sensible place.

Use `subgraph` to cluster related steps (e.g., everything inside one sprint, one deployment stage, one service boundary) — it's the Mermaid equivalent of a grouping box, and can be styled with its own `style SubgraphName fill:...,stroke:...` line. Don't nest subgraphs more than one level deep; it gets hard to read fast.

## Workflow

1. **Identify the underlying structure** and pick the diagram type from the table above before writing any syntax.
2. **Assign category colors** to the roles present (inputs, process steps, decisions, outputs, feedback) — sketch this out in a sentence or two before writing classDefs, same as content-diagrams' "sketch the motif reasoning" step, so the choice is auditable if Ibrahim wants to adjust one piece.
3. **Write the diagram**, starting with the `%%{init: ...}%%` directive, then structure, then `classDef`/`class` assignments (or themeVariables for types that don't support per-node classes).
4. **Self-check the syntax** — every node ID used in an edge is defined somewhere; every `classDef` has both `fill` and `color` set; brackets/quotes are balanced; no paragraph-length label. No rendering, no screenshotting.
5. **Save as a `.mermaid` file** via `create_file` so it renders inline as an artifact, using a descriptive slug: `/mnt/user-data/outputs/<slug>.mermaid`. Present with `present_files`.
6. If Ibrahim needs the diagram as a portable static image (for embedding somewhere that won't render Mermaid, or for archival), say so plainly: this environment doesn't reliably run headless Mermaid-to-image export (it depends on a Chromium download that the sandboxed network usually can't reach). Point to mermaid.live for a manual export, or switch to `content-diagrams` if the real requirement is a standalone graphic.

## What not to do

- Don't leave a `classDef`'s `color` unset after overriding `fill` — that's the exact contrast bug this skill exists to avoid.
- Don't mix the dark-fill and light-fill palette recipes within one diagram.
- Don't default every request to `flowchart` — pick the type that matches the actual structure (sequence, state, ER, etc.).
- Don't reintroduce content-diagrams' render/crop/verify loop here — it's solving a problem Mermaid's layout engine doesn't have.
- Don't put paragraph-length text in a node label; wrap with `<br/>` or cut the content.
- Don't nest subgraphs more than one level.
- Don't promise a clean PNG/SVG export from this sandbox without caveating that headless Mermaid rendering may not work here.
