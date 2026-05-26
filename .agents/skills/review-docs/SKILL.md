---
name: review-docs
description: Detect documentation drift. Compares code changes against docs/diagrams and reports what is stale or missing. Read-only — does not modify files.
allowed-tools: Read, Grep, Glob, Bash
---

# Review Documentation: Drift Analysis

## Overview

You act as a **Documentation Auditor**. Your job is to find what documentation is stale, missing, or inconsistent with the current code. You do NOT fix anything — you produce a report.

## The Process

### Step 1: Gather Evidence
1. Run `git diff --name-only main...HEAD` to see all modified files.
2. Read the modified source files to understand what changed.
3. Categorize changes:
   - **Architectural:** New modules, services, classes, or infrastructure components
   - **API:** New or changed endpoints, function signatures, CLI commands
   - **Configuration:** New env vars, config options, dependencies
   - **Behavioral:** Changed logic, algorithms, or workflows

### Step 2: Scan Existing Documentation
1. Find all documentation files: `docs/**/*.md`, `docs/**/*.rst`, `README.md`
2. Find all diagram scripts: `*.py` files that import `diagrams`
3. Find all image prompt files: `docs/images/prompts/*.md`
4. Check MkDocs config if present: `mkdocs.yml`

### Step 3: Drift Analysis
For each category of change, check:

#### Text Documentation
- Do README/docs mention the new features/APIs?
- Are any documented features now removed or changed?
- Are code examples still valid?
- Are install/setup instructions still correct?

#### Architecture Diagrams
- Do diagram scripts include all current components?
- Are removed components still in diagrams?
- Are new connections/flows represented?

#### Generated Images
- Are there prompt files for new concepts that need illustration?
- Are existing prompt descriptions still accurate?

### Step 4: The Report

Output in this exact format:

> **Documentation Drift Report**
>
> **1. Text Documentation:**
> * Status: [UP TO DATE / DRIFT DETECTED]
> * Issues: (list specific files and what needs updating)
>
> **2. Architecture Diagrams:**
> * Status: [UP TO DATE / DRIFT DETECTED / NO DIAGRAMS FOUND]
> * Issues: (list components missing from or stale in diagram scripts)
>
> **3. Generated Images:**
> * Status: [UP TO DATE / DRIFT DETECTED / NO PROMPTS FOUND]
> * Issues: (list prompts that need creating or updating)
>
> **4. MkDocs Config:**
> * Status: [UP TO DATE / DRIFT DETECTED / NOT CONFIGURED]
> * Issues: (new pages not in nav, broken references)
>
> **Actions Required:**
> * [FIX-DOCS] (list text documentation fixes needed)
> * [GENERATE-DIAGRAMS] (list diagram updates needed)
> * [GENERATE-IMAGES] (list image generation needed)

## Critical Rules
- **Read-only.** Do NOT edit any files. Only report.
- **Be specific.** Name the exact file, line, and what needs changing.
- **Tag actions.** Use [FIX-DOCS], [GENERATE-DIAGRAMS], [GENERATE-IMAGES] tags so downstream skills know what to do.
