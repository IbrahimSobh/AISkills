# content-mermaid

Creates and styles Mermaid diagrams (flowcharts, sequence, state, ER, class, Gantt, mindmap, timeline) for technical processes and architectures. It picks the diagram type that fits the content, applies a consistent high-contrast color system, and outputs source that renders natively on GitHub, GitLab, Notion, Obsidian and docs sites. Built for developers and technical writers who want readable diagrams without hand-tuning layout.

## When to use it

- You need a flowchart, sequence diagram, state machine or ER diagram for a README or docs page.
- You want an existing Mermaid diagram restyled, recolored or made more readable.
- You are visualizing a software process such as a CI/CD pipeline, git workflow or API flow.

## Example request

> "Make a Mermaid diagram of a typical CI/CD pipeline: a developer pushes code, CI builds and runs tests, failed tests go back to the developer, passing builds deploy to staging, a manual approval gate, then production deploy."

## Example output

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontFamily': 'Trebuchet MS, Verdana, Arial, sans-serif', 'fontSize': '16px', 'primaryColor': '#1e3a5f', 'primaryTextColor': '#ffffff', 'primaryBorderColor': '#0d1f33', 'lineColor': '#666666', 'background': '#ffffff' } } }%%
flowchart LR
    dev["Developer<br/>pushes code"]
    ci["CI builds<br/>and runs tests"]
    pass{"Tests<br/>pass?"}
    staging["Deploy to<br/>staging"]
    gate{"Manual<br/>approval"}
    prod["Deploy to<br/>production"]

    dev --> ci
    ci --> pass
    pass -->|pass| staging
    pass -.->|fail| dev
    staging --> gate
    gate -->|approved| prod

    classDef input fill:#1e3a5f,stroke:#0d1f33,stroke-width:2px,color:#ffffff
    classDef process fill:#1b5e3a,stroke:#0d3320,stroke-width:2px,color:#ffffff
    classDef decision fill:#8a5a00,stroke:#4d3200,stroke-width:2px,color:#ffffff
    classDef output fill:#5b2a86,stroke:#341650,stroke-width:2px,color:#ffffff

    class dev input
    class ci,staging process
    class pass,gate decision
    class prod output

    linkStyle 3 stroke:#b3261e,stroke-width:2px
```

- **Diagram type:** a `flowchart LR` fits a sequential pipeline with a branch and a loop; left-to-right reads like a pipeline.
- **Colors:** blue is the input (developer), green is active work (build, tests, staging deploy), amber is decisions and gates, purple is the final output (production). Every class sets both fill and text color for contrast.
- **Dashed red arrow:** the failed-tests path is a feedback loop, not the normal flow, so it is dashed and red while the main path stays solid.

_Last run: 2026-10-12 · Claude Sonnet 5.5_

## Install

```bash
cp -r content-mermaid ~/.claude/skills/
```

Full instructions for the agent: [SKILL.md](SKILL.md)
