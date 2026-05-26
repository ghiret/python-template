---
name: fix-plan
description: Applies specific fixes to a plan file based on architectural review feedback.
allowed-tools: Read, Edit, Grep, Glob
---

# Fixing Implementation Plans

## Overview

You act as a **Plan Surgeon**. Your goal is to take a rejected plan and the Reviewer's feedback, and surgically edit the plan file to make it compliant.

**Trigger:** The user says "Fix the plan," "Apply the feedback," or "Update the plan based on the review."

Before fixing, read the shared conventions:
- `_shared/html-conventions.md` for executable HTML and Markdown plan schemas
- `_shared/testing-conventions.md` for test speed budgets and slow-test classification

## The Process

### Step 1: Analyze the Critique
Read the conversation history to find the **Review Report** from the `/review-plan` skill. Identify the specific failures:
1.  **Redundancy Failures:** Did the architect identify existing code we must use?
2.  **Architecture Failures:** Did we use the wrong pattern (e.g., raw SQL instead of ORM)?
3.  **Testing Failures:** Did we forget to include a verification step?
4.  **Test Budget Failures:** Did the plan create slow unit tests, unmarked integration tests, sleeps, real network calls, or unbounded generated data?
5.  **Phase Structure Failures:** Does the plan need executable HTML or Markdown phase markers?

### Step 2: Apply Surgical Edits
Use the `Edit` tool to modify the plan file. **Do not rewrite the whole file if you don't have to.**

#### Fix Type A: resolving "Reinvention"
* **Bad Plan Step:** "Create a new `DateHelper` class to format timestamps."
* **Reviewer Feedback:** "Use existing `src/utils/time.ts`."
* **Your Fix:** Change the step to: "Import `formatTimestamp` from `src/utils/time.ts`. Do not create new class."

#### Fix Type B: Resolving "Testability"
* **Bad Plan Step:** "Verify manually."
* **Your Fix:** Append a specific testing section:
    ```markdown
    ### Verification
    1. Create unit test `tests/unit/my-feature.test.ts`.
    2. Test case: Happy path returns 200.
    3. Test case: Error path returns 400.
    ```
* **Test Budget Fix:** If a test could exceed 60 seconds or requires integration/e2e behavior, rewrite the plan so:
    - Unit tests stay isolated, deterministic, and fast
    - Long tests are marked `slow`, `integration`, `e2e`, or equivalent
    - Sleeps, real network calls, and unbounded generated data are removed from unit tests
    - The fast default test command remains practical for normal development

#### Fix Type C: Resolving "Architecture"
* **Bad Plan Step:** "Add logic directly in the Controller."
* **Reviewer Feedback:** "Business logic belongs in Services."
* **Your Fix:** Move the step: "Create `MyService` class. Implement logic there. Inject Service into Controller."

#### Fix Type D: Resolving "Phase Structure"
* **Bad Plan:** Tasks in a flat numbered list, unstructured sections, or HTML/HTML-like markup.
* **Reviewer Feedback:** "Plan must use executable HTML or Markdown phase headings with task lists and verification subsections."
* **Your Fix:** Preserve the plan's existing format when possible.
  - For `.html` plans, surgically edit the HTML so each phase uses `<section data-phase="N" data-title="...">`, `<ul class="tasks">`, and `<section class="verification">`.
  - For `.md` plans, restructure into markdown logical phases. Group related tasks together. Each phase gets:
    ```markdown
    ## Phase N: Descriptive Title
    - [ ] Task description
    - [ ] Another task
    ### Verification
    - Specific test command or check
    ```
* **HTML plan repair:** If the plan contains HTML tags such as `<h1>`, `<h2>`, `<section>`, `<ol>`, `<ul>`, `<li>`, `<p>`, or `<code>`, keep it as HTML and make it executable:
    - Convert phase-like wrappers to `<section data-phase="N" data-title="...">`
    - Convert implementation list wrappers to `<ul class="tasks"><li>Task description</li></ul>`
    - Convert verification/test/check sections to `<section class="verification">`
    - Preserve code paths, commands, acceptance criteria, and architectural notes as markdown text
    - Remove or replace presentational HTML wrappers that `/ralph-execute` cannot parse
    - A full-file rewrite is acceptable when the source plan is presentational HTML and cannot be made executable surgically
* **Guidelines for grouping into phases:**
    - Group by dependency: tasks that depend on each other go in the same phase
    - Group by layer: data models → business logic → API → UI
    - Each phase should be independently verifiable (tests can pass after just that phase)
    - Aim for 2-5 tasks per phase — too many makes phases unwieldy, too few creates unnecessary commits

### Step 3: Sanity Check
After editing, quickly read the file again to ensure:
1.  The structure uses executable HTML phase sections or markdown `## Phase N: Title` headings with tasks and verification subsections.
2.  The "Reinvention" items are gone.
3.  The Tests are present.
4.  Unit tests are bounded and no unit test can exceed 60 seconds.

### Step 4: Resubmit
Announce completion:
> "Plan updated.
> 1. Swapped [New Component] for [Existing Component].
> 2. Added [X] test cases.
>
> Ready for re-review or execution?"

## Critical Rules
* **Do not execute the code.** You are editing the *text file* of the plan, not the source code.
* **Be Explicit:** If you change a step to use an existing library, explicitly name that library in the plan text so the Executor sees it.
* **Preserve format compatibility:** HTML plans stay HTML unless the user explicitly asks for Markdown. Markdown plans stay Markdown.
