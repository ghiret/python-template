---
name: verifying-documentation
description: Synchronizes docs with code. Specializes in "Diagrams as Code" (Python) to generate architectural visuals. Verifies Sphinx/MkDocs and ensures generated PNGs match the actual implementation.
allowed-tools: Read, Grep, Glob, Bash, LS
---

# Verifying Documentation (Diagrams as Code Edition)

## Overview

You act as a **Technical Writer & Visualization Expert**.
**Core Philosophy:** Documentation is Code. Diagrams are Code.
**Tooling:** You prefer the Python `diagrams` library over text-based tools (Mermaid) for architectural flows.

**Trigger:** When asked to "update docs", "visualize the architecture", or "sync docs".

## The Process

### Step 1: Ecosystem & Dependency Check
1.  **Check for Graphviz:** Run `dot -V`. If missing, warn the user.
2.  **Check for Diagrams lib:** Check `pip list` or try `python -c "import diagrams"`.
3.  **Identify Provider:** Scan `package.json` or `go.mod` or imports to see if this is AWS, GCP, K8s, or OnPrem. This determines which `diagrams` nodes to import.

### Step 2: Drift Analysis
Compare **Code** vs. **Docs**.
1.  Run `git diff --name-only main...HEAD` to see modified architectural components.
2.  Identify "Invisible Changes": Did we add a cache? A queue? A load balancer?
3.  **The Rule:** If a component exists in the infrastructure code, it **must** exist in the diagram script.

### Step 3: Generate "Diagrams as Code"
Do not edit PNGs manually. Edit the Python script that generates them.

1.  **Locate Script:** Look for `*.py` files that import `diagrams`.
2.  **Edit/Create Script:**
    * **Import:** Use specific providers (e.g., `from diagrams.aws.compute import EC2`).
    * **Cluster:** Use `with Cluster("Name"):` to group related services.
    * **Flow:** Use `>>` for flow direction.
    * **Attributes:** Use `graph_attr = {"concentrate": "true"}` if edges get messy.
3.  **Execute:** Run the script: `python docs/diagrams/architecture.py`.
4.  **Output:** Ensure a `.png` was generated.

### Step 4: Visual Review & Verification
1.  **Logic Check:** Read the Python script again. Does `Service A >> Service B` match the actual API calls in the code?
2.  **Visual Check:**
    * *Agent Action:* Check the file size of the PNG to ensure it's not empty.
    * *User Interaction:* **Crucial Step.** explicit ask:
        > "I have generated `architecture.png`. Please open this file. Does it visually represent what you intended? Does the grouping in the 'Service Cluster' look right?"

### Step 5: Text Documentation Update
1.  Update `README.md` or Sphinx `.rst` files to embed the new image.
2.  Ensure text descriptions match the new diagram nodes.

### Step 6: The Report
Output in this format:

> **Documentation & Visuals Report**
>
> **1. Architectural Drift:**
> * Detected new components: [List components found in code]
>
> **2. Visual Updates (Diagrams as Code):**
> * Updated script: `docs/architecture.py`
> * Generated artifact: `docs/architecture.png`
> * **Action Required:** Please review the generated PNG.
>
> **3. Text Sync:**
> * Updated [Filename] to reflect new architecture.

## Diagrams Reference Guide (Python)

**Standard Imports:**
```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.onprem.network import Nginx
