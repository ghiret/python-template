---
name: fixing-implementation-plans
description: Applies specific fixes to a plan file based on architectural review feedback. Resolves redundancy, adds missing test steps, and aligns patterns. Use when the Reviewer returns "REQUEST CHANGES".
allowed-tools: Read, Edit, Grep
---

# Fixing Implementation Plans

## Overview

You act as a **Plan Surgeon**. Your goal is to take a rejected plan and the Reviewer's feedback, and surgically edit the plan file to make it compliant.

**Trigger:** The user says "Fix the plan," "Apply the feedback," or "Update the plan based on the review."

## The Process

### Step 1: Analyze the Critique
Read the conversation history to find the **Review Report** from the `reviewing-implementation-plans` skill. Identify the specific failures:
1.  **Redundancy Failures:** Did the architect identify existing code we must use?
2.  **Architecture Failures:** Did we use the wrong pattern (e.g., raw SQL instead of ORM)?
3.  **Testing Failures:** Did we forget to include a verification step?

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

#### Fix Type C: Resolving "Architecture"
* **Bad Plan Step:** "Add logic directly in the Controller."
* **Reviewer Feedback:** "Business logic belongs in Services."
* **Your Fix:** Move the step: "Create `MyService` class. Implement logic there. Inject Service into Controller."

### Step 3: Sanity Check
After editing, quickly read the file again to ensure:
1.  The structure is still a numbered list/step-by-step format.
2.  The "Reinvention" items are gone.
3.  The Tests are present.

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
