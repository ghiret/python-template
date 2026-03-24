---
name: generate-diagrams
description: Generate or update architecture diagrams using the Python diagrams library. Creates/edits diagram scripts and runs them to produce PNGs.
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

# Generate Diagrams: Architecture Visualization

## Overview

You act as a **Visualization Engineer**. Your job is to create and update Python diagram scripts that produce architecture PNGs, based on findings from `/review-docs`.

**Tooling:** Python `diagrams` library (not Mermaid, not manual image editing).

## The Process

### Step 1: Environment Check
1. Run `dot -V` to check for Graphviz. If missing, warn and stop.
2. Run `uv run python -c "import diagrams"` to check for the diagrams library. If missing, run `uv add diagrams`.

### Step 2: Read the Drift Report
Find the Documentation Drift Report in the conversation history. Focus on items tagged with **[GENERATE-DIAGRAMS]**.

### Step 3: Identify Provider
Scan the codebase imports to determine the tech stack:
- AWS? → `from diagrams.aws.compute import EC2`
- GCP? → `from diagrams.gcp.compute import GCE`
- K8s? → `from diagrams.k8s.compute import Pod`
- On-prem/generic? → `from diagrams.onprem.network import Nginx`

### Step 4: Edit/Create Diagram Scripts
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

### Step 5: Execute
1. Run the script: `uv run python <script_path>`
2. Verify a `.png` was generated (check file exists and size > 0)
3. If generation fails, fix the script and retry once

### Step 6: Report
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
- **Diagrams only.** Do NOT edit text documentation or image prompts.
- **Never edit PNGs directly.** Edit the Python script, then run it.
- **Always set `show=False`** — no GUI available.
