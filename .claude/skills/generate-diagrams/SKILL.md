---
name: generate-diagrams
description: Generate or update architecture diagrams using Python diagrams PNGs or inline SVG inside HTML artifacts.
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

# Generate Diagrams: Architecture Visualization

## Overview

You act as a **Visualization Engineer**. Your job is to create and update architecture diagrams based on findings from `/review-docs`.

**Tooling:** Choose the right output path:
- Use Python `diagrams` PNGs for complex provider-icon topologies, cloud architecture, or diagrams with more than about 30 nodes.
- Use hand-authored inline SVG for diagrams that live inside an HTML plan, report, explainer, or prototype and have about 30 nodes or fewer.
- Do not use Mermaid unless the repository already depends on it for docs.

## The Process

### Step 1: Choose Diagram Path

Use **SVG-in-HTML** when:
- The target artifact is an `.html` file
- The diagram is conceptual, flow-oriented, or annotation-heavy
- The diagram has about 30 nodes or fewer
- The user needs a self-contained browser-readable artifact

Use **Python diagrams PNG** when:
- The diagram needs provider icons from AWS, GCP, Kubernetes, or on-prem libraries
- The topology is large or operational
- The repository already has diagram scripts
- The image should be embedded in Markdown/MkDocs docs

### Step 2: Environment Check

Skip this step if using SVG-in-HTML.

1. Run `dot -V` to check for Graphviz. If missing, warn and stop.
2. Run `uv run python -c "import diagrams"` to check for the diagrams library. If missing, run `uv add diagrams`.

### Step 3: Read the Drift Report
Find the Documentation Drift Report in the conversation history or read the latest `*.html` report from `agent_docs/reports/drift/`. Focus on items tagged with **[GENERATE-DIAGRAMS]**.

### Step 4A: Create Inline SVG In HTML

When using SVG-in-HTML:

1. Read the target HTML artifact.
2. Add or update a `<section>` containing an inline `<svg>`.
3. Use a stable `viewBox`, semantic labels, and accessible title/description.
4. Keep CSS inline in the artifact.
5. Use simple shapes, connectors, arrow markers, and labels.
6. Verify the SVG is self-contained and does not reference external assets.

Skeleton:

```html
<section class="diagram" aria-labelledby="diagram-title">
  <h2 id="diagram-title">System Flow</h2>
  <svg viewBox="0 0 960 420" role="img" aria-labelledby="svg-title svg-desc">
    <title id="svg-title">System Flow</title>
    <desc id="svg-desc">Request flow from API to worker and database.</desc>
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
              markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z"></path>
      </marker>
    </defs>
    <rect x="40" y="80" width="180" height="72" rx="8"></rect>
    <text x="130" y="122" text-anchor="middle">API</text>
    <line x1="220" y1="116" x2="360" y2="116" marker-end="url(#arrow)"></line>
  </svg>
</section>
```

Guidelines:
- Use `viewBox` instead of fixed pixel-only sizing.
- Keep labels short and readable.
- Use groups (`<g>`) for repeated node patterns.
- Use `marker` arrows for flows.
- Avoid decorative complexity that makes the diagram harder to inspect.

### Step 4B: Identify Provider For Python Diagrams

Scan the codebase imports to determine the tech stack:
- AWS? → `from diagrams.aws.compute import EC2`
- GCP? → `from diagrams.gcp.compute import GCE`
- K8s? → `from diagrams.k8s.compute import Pod`
- On-prem/generic? → `from diagrams.onprem.network import Nginx`

### Step 5: Edit/Create Diagram Scripts

When using Python diagrams:

1. Look for existing `*.py` files that import `diagrams`
2. If updating: use the Edit tool to add/remove/modify components
3. If creating: write a new script following this pattern:

```python
from diagrams import Diagram, Cluster, Edge
# Import specific providers based on Step 3

with Diagram("Architecture", filename="docs/diagrams/architecture", show=False):
    with Cluster("Service Group"):
        svc = ComponentType("Service Name")

    other >> Edge(label="calls") >> svc
```

**Guidelines:**
- Use `Cluster()` to group related services
- Use `>>` for flow direction
- Use `Edge(label="...")` for labeled connections
- Set `graph_attr = {"concentrate": "true"}` if edges overlap
- Always set `show=False` (we're running headless)

### Step 6: Execute Or Validate

For Python diagrams:

1. Run the script: `uv run python <script_path>`
2. Verify a `.png` was generated (check file exists and size > 0)
3. If generation fails, fix the script and retry once

For inline SVG:

1. Re-read the HTML artifact.
2. Confirm the `<svg>` has a `viewBox`, title/description, and no external references.
3. Confirm the labels and connectors match the surrounding explanation.

### Step 7: Report
> "Diagrams updated:
> 1. Updated `docs/diagrams/architecture.py`: added {component}
> 2. Generated `docs/diagrams/architecture.png` ({size} KB)
>
> **Please review the generated PNG(s) visually.**"

## Diagrams Reference

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, DynamoDB
from diagrams.aws.network import ELB, APIGateway
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Python
```

## Critical Rules
- **Diagrams only.** Do NOT make unrelated text documentation or image prompt changes.
- **Never edit PNGs directly.** Edit the Python script, then run it.
- **Always set `show=False`** for Python diagrams — no GUI available.
- **Keep inline SVG self-contained.** No external assets, scripts, or stylesheets.
