# high-fidelity-summarizer

Compresses technical, legal, financial, or analytical text to about 25% of its length while keeping every named entity, number, claim, and the source's order and formatting. The prose is rewritten; names and figures are not. For readers who need a summary that can stand in for the original.

## When to use it

- You need a shorter version of a contract, report, paper, or transcript that still carries the exact terms and figures.
- Precision outranks readability, so loose paraphrase is not acceptable.
- You want a measured result: the skill ends with a script-verified word count and percentage.

## Example request

> Summarize this section with high fidelity: [pasted text]

<details>
<summary>Input text (204 words)</summary>

> ## Why there's no verification loop here
>
> `content-diagrams` spends most of its effort on geometry: an SVG line, box, or label is just numbers Claude computed, and computed numbers can be wrong — hence render, screenshot, crop, and check.
>
> Mermaid removes that failure mode entirely. Node width, text wrapping, arrow paths, and collision avoidance between elements are the *renderer's* job, not Claude's — the renderer will not place a label on top of a box or route a line through a shape. Re-deriving that verification loop here (screenshotting the rendered diagram, cropping, checking overlaps) would just burn tokens and latency confirming something the tool already guarantees.
>
> What can still go wrong is entirely different, and entirely textual:
> - Broken syntax (unclosed brackets, a reserved word used as a node ID, mismatched arrow types)
> - An edge referencing a node ID that's never defined
> - Poor color contrast (a fill and text color that don't actually read against each other)
> - The wrong diagram type for the content's actual structure
>
> So verification here means: read the syntax once for correctness, check every classDef pairs a fill with a genuinely contrasting text color, and confirm the diagram type matches what's being modeled. No image rendering required.

</details>

## Example output

> ## Why there's no verification loop here
>
> Unlike `content-diagrams`, Mermaid's renderer owns layout and collisions, so screenshot checks waste tokens.
>
> Remaining failures are textual:
> - Broken syntax
> - Undefined node IDs in edges
> - Poor color contrast
> - Wrong diagram type
>
> Verify: read syntax once, check classDef contrast, confirm diagram type. No rendering.
>
> ---
> Summary number of words: 53
> Summary size percentage of the original : 26.0%

_Last run: 2026-10-12 · Claude Sonnet 5.5_

## Install

```bash
cp -r high-fidelity-summarizer ~/.claude/skills/
```

Full instructions for the agent: [SKILL.md](SKILL.md)
