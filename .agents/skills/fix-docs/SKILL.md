---
name: fix-docs
description: Update text documentation (README, markdown, rst, html) based on a documentation drift report. Does not touch diagrams or images.
allowed-tools: Read, Edit, Grep, Glob
---

# Fix Documentation: Text Updates

## Overview

You act as a **Technical Writer**. Your job is to update text documentation to match the current state of the code, based on findings from `/review-docs`.

Before fixing, read `_shared/html-conventions.md` for drift report artifact locations.

## The Process

### Step 1: Read the Drift Report
Find the Documentation Drift Report in the conversation history or read the latest `*.html` report from `agent_docs/reports/drift/`. Focus on items tagged with **[FIX-DOCS]**.

### Step 2: Apply Fixes
For each [FIX-DOCS] item:

1. Read the target documentation file
2. Apply surgical edits using the Edit tool — do NOT rewrite entire files
3. Ensure:
   - New features/APIs are documented
   - Removed features are cleaned up
   - Code examples are valid and runnable
   - Install/setup instructions are current
   - Links and references are not broken
   - Markdown, RST, and HTML documentation files keep their existing format

### Step 3: MkDocs Config
If the drift report flagged MkDocs issues:
1. Read `mkdocs.yml`
2. Add new pages to the nav
3. Fix broken references

### Step 4: Verify
1. Re-read each edited file to confirm the changes are correct
2. If MkDocs is configured, run `uv run mkdocs build` to check for errors

### Step 5: Report
Announce what was fixed:
> "Documentation updated:
> 1. Updated README.md: added section on {feature}
> 2. Fixed docs/api.md: updated endpoint signatures
> 3. Added docs/guides/new-feature.md
>
> Documentation text is now in sync with code."

## Critical Rules
- **Text only.** Do NOT edit diagram scripts or image prompts. Those are handled by `/generate-diagrams` and `/generate-images`.
- **Surgical edits.** Do not rewrite files unnecessarily.
- **Follow the report.** Only fix what was flagged — don't go looking for extra issues.
- **Format preserving.** Support `.md`, `.rst`, and `.html` docs without converting formats unless explicitly requested.
