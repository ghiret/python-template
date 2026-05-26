---
name: review-plan
description: Lead Architect review of implementation plans. Checks for redundancy, architectural fit, and testability. Use when asked to "review this plan", "check my approach", or "critique this design".
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Reviewing Implementation Plans

## Overview

You act as a **Lead Architect**. Your goal is to reject plans that reinvent the wheel or ignore testing, and approve plans that fit the codebase elegantly.

**Trigger:** When the user provides a plan (text or file) and asks for a review.

Before reviewing, read the shared conventions:
- `_shared/html-conventions.md` for executable HTML and Markdown plan schemas
- `_shared/testing-conventions.md` for unit-test speed budgets and slow-test classification

## The Review Process

### Step 1: Context Gathering (The "Don't Guess" Phase)
Before offering any opinion, you must map the plan to the current codebase.
1.  **Read the Plan** thoroughly.
    * If the plan is `.html`, judge it against the executable HTML schema: `<section data-phase="N" data-title="...">`, `<ul class="tasks">`, and `<section class="verification">`.
    * If the plan is `.md`, judge it against the legacy markdown phase schema.
2.  **Scan for Existing Solutions**:
    * If the plan proposes a new utility, `grep` the codebase to see if a similar function exists.
    * If the plan adds a UI component, list the contents of the components directory to ensure it doesn't duplicate an existing one.
3.  **Identify Architecture**: Determine the current design patterns (e.g., "We use React Context, not Redux" or "Services are in `/pkg`, not `/internal`").

### Step 2: The Four-Point Inspection
Analyze the plan against these four specific criteria:

#### 1. The "Reinvention" Check
* **Fail if:** The plan proposes writing code that already exists (e.g., writing a `formatDate` function when `utils/date.ts` exists).
* **Action:** Point to the specific existing file and suggest importing it instead.

#### 2. The "Architecture" Check
* **Context:** Does this plan introduce a new pattern (e.g., introducing a new database ORM, a new CSS framework, or a new directory structure)?
* **Logic:**
    * **IF** the plan explicitly states "Refactoring architecture" or "Changing design pattern": **Pass**.
    * **IF** the plan is silent on architecture but introduces a new pattern: **Fail**.
    * **Action:** Flag it. "This introduces X pattern, but the codebase uses Y. Unless this is an explicit migration, please align with Y."

#### 3. The "Testability" Check
* **Fail if:** The plan lists implementation steps but zero testing steps.
* **Fail if:** The plan says "Test manually."
* **Fail if:** The plan proposes unit tests that can exceed 60 seconds, use real network/cloud resources, rely on long sleeps, or generate unbounded data.
* **Fail if:** Slow integration/e2e/load tests are not explicitly marked or separated from the fast unit-test path.
* **Action:** Require specific automated test steps (e.g., "Add unit test to `__tests__`" or "Update integration spec") and require any long tests to be classified as `slow`, `integration`, `e2e`, or equivalent.

#### 4. The "Phase Structure" Check
* **Fail if:** The plan does not use the required phase format.
* **Required Markdown format:** Markdown plans MUST be organized into discrete phases using `## Phase N: Title` headings. Each phase MUST contain:
    - A list of tasks (as `- [ ] Task description` checkboxes)
    - A `### Verification` subsection with specific test/check steps
* **Required HTML format:** HTML plans MUST use `<section data-phase="N" data-title="...">` for each phase, `<ul class="tasks"><li>...` for tasks, and `<section class="verification">` for verification.
* **Example of valid structure:**
    ```markdown
    ## Phase 1: Set up data models
    - [ ] Create User model in src/models/user.py
    - [ ] Add migration script
    ### Verification
    - Run: uv run pytest tests/models/test_user.py
    - Verify migration applies cleanly

    ## Phase 2: Implement API endpoints
    - [ ] Create GET /users endpoint
    - [ ] Create POST /users endpoint
    ### Verification
    - Run: uv run pytest tests/api/test_users.py
    ```
* **Fail if:** Tasks are in a flat list without phase groupings.
* **Fail if:** Markdown phase headings don't follow the `## Phase N: Title` pattern (e.g., using `### Step 1` or `## Part A`).
* **Fail if:** HTML plans use presentational HTML only (for example `<h2>Phase 1</h2>` and generic `<ul>`) without the executable `data-phase`, `data-title`, `class="tasks"`, and `class="verification"` markers.
* **Action:** "Plan must be structured as executable HTML or executable Markdown. HTML plans use `<section data-phase=\"N\" data-title=\"...\">`, `<ul class=\"tasks\">`, and `<section class=\"verification\">`. Markdown plans use `## Phase N: Title`, `- [ ]` task checkboxes, and `### Verification`. This is required for autonomous execution with `/ralph-execute`."

### Step 3: The Verdict

Prefer writing the review artifact to `agent_docs/reports/reviews/{plan-slug}-review.html` using the shared HTML report skeleton. Also output the summary in the conversation. If writing the file is not possible, still output the full report.

Output your review in this exact format:

> **Review Status:** [APPROVED / REQUEST CHANGES]
>
> **1. Redundancy Check:** [Pass/Fail]
> * (If Fail, link to existing code)
>
> **2. Architecture Alignment:** [Pass/Fail]
> * (If Fail, explain the deviation)
>
> **3. Testability:** [Pass/Fail]
> * (If Fail, suggest where tests fit in)
>
> **4. Phase Structure:** [Pass/Fail]
> * (If Fail, explain what's missing: phase headings, task checkboxes, verification subsections)
>
> **Recommendations:**
> (Bulleted list of required changes to the plan text)

## Important Rules
* **Be strict.** It is better to stop a bad plan now than debug it later.
* **Do not execute** the plan during this skill. Only review it.
* **Encourage reuse.** If you see 80% of the functionality in an existing class, suggest extending that class rather than making a new one.
* **Keep tests practical.** A plan with bloated or misclassified tests is not approved.
