---
name: html-artifact
description: Create self-contained HTML artifacts for exploration grids, PR explainers, design prototypes, reports, and throwaway editors.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# HTML Artifact: Self-Contained Agent Outputs

## Overview

You create self-contained HTML artifacts for agent work that needs to be read,
shared, compared, or briefly interacted with outside the conversation. Use this
skill for artifacts that are not executable plans and are not the standard
review/verify/drift reports covered by `_shared/html-conventions.md`.

**Trigger:** The user asks for an HTML artifact, explainer, comparison grid,
throwaway editor, interactive prototype, annotated PR view, or browser-readable
report.

Before creating an artifact, read `_shared/html-conventions.md` for artifact
locations and report conventions.

## Where Artifacts Go

Write artifacts under `agent_docs/` unless the user specifies a committed docs
location. Suggested locations:

- Exploration grids: `agent_docs/explorations/*.html`
- PR explainers: `agent_docs/reports/reviews/*.html`
- Design prototypes: `agent_docs/prototypes/*.html`
- Throwaway editors: `agent_docs/tools/*.html`
- One-off reports: `agent_docs/reports/*.html`

Generated agent artifacts under `agent_docs/` are ignored by default and should
not be committed unless the user explicitly asks.

## Artifact Patterns

### Exploration Grid

Use when comparing multiple options side by side.

- Show each variant in a labeled column or card.
- Include the tradeoff each variant is testing.
- Keep source prompts, assumptions, and selection criteria visible.
- Make differences scannable without relying on color alone.

### PR Explainer or Diff Renderer

Use when explaining a code change to humans.

- Summarize intent, risk, and verification.
- Include changed files and important snippets.
- Use margin notes or callouts for architectural decisions.
- Preserve stable file paths and commands as text/code.

### Design Prototype

Use when a lightweight interactive UI helps evaluate an idea.

- Keep all CSS and JavaScript inline.
- Use simple controls such as sliders, toggles, tabs, and copy buttons.
- Avoid external CDNs, remote fonts, or network dependencies.
- Include enough labels for someone to understand the prototype in a browser.

### Throwaway Editor

Use when the artifact helps produce JSON, Markdown, diffs, prompts, or config.

- Include a clear copy-out affordance.
- Make generated output visible in a textarea or code block.
- Never imply the artifact writes back to the repository.
- Keep state local to the page.

### Single-Purpose Report

Use when the user needs a readable standalone summary.

- Use the shared HTML report skeleton where practical.
- Include stable text markers if another skill may consume the report.
- Include source paths, commands, dates, and assumptions.

## HTML Requirements

- Produce one self-contained `.html` file.
- Use inline CSS and optional inline JavaScript.
- Do not require browser automation, build tools, external assets, or network
  access.
- Keep styling restrained and readable.
- Use semantic elements: `main`, `section`, `article`, `table`, `pre`, `code`.
- Escape user-provided content that is displayed as HTML.
- Prefer plain text/code markers for data that downstream skills may grep.

## Process

1. Clarify the artifact type from the user's request.
2. Choose an output path under `agent_docs/`.
3. Gather only the source files or context needed for the artifact.
4. Create or update the self-contained HTML file.
5. Re-read the artifact to check:
   - it has a doctype, `<html>`, `<head>`, and `<body>`
   - it does not reference external assets
   - interactive controls, if any, have inline scripts
   - important paths, commands, and assumptions are present
6. Report the artifact path and a concise summary of what it contains.

## Critical Rules

- Do NOT replace executable plan or standard report schemas with this skill.
  Use `_shared/html-conventions.md` for plans, plan reviews, verification
  reports, and drift reports.
- Do NOT add dependencies.
- Do NOT put generated scratch artifacts outside `agent_docs/` unless requested.
- Do NOT create an artifact that silently performs repository writes.
