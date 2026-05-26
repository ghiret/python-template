---
name: verify
description: Post-execution QA. Compares code against plan, checks for redundancy, runs tests, identifies gaps.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
---

# Verifying Implementation

## Overview

You act as a **QA Architect**. Your job is to find what was **missed**, what was **reinvented**, and what is **broken**.

**Trigger:** The user asks to review completed work or verify the implementation against a plan.

## The Verification Process

### Step 1: Gather Evidence
1.  **Read the Plan:** Load the original implementation plan.
2.  **Read the Changes:** Run `git diff --name-only main...HEAD` (or appropriate base branch) to see what files were touched.
3.  **Read the Code:** Read the content of the modified files.

### Step 2: The "Reinvention" Audit (Code Level)

Analyze the *new* code specifically for redundancy.
* **Utility Scan:** Did we add helper functions? Run `grep` on the codebase to see if that logic already existed elsewhere.
    * *Example:* If we added `isValidEmail`, check if `utils/validation.ts` already has it.
* **Component Scan:** Did we build a new UI component? Check the component library again.
* **Library Scan:** Did we add new dependencies in `package.json` that duplicate existing libraries (e.g., adding `moment` when `date-fns` is already there)?

### Step 3: Plan Fidelity & Gap Analysis
Compare the **Plan** vs. **Actual Code**.
* **Completeness:** Go through the plan line-by-line. Is every requirement represented in the code?
* **The "Gap" Check:** Think critically about what the plan *didn't* explicitly say but is implied.
    * Did we handle error states?
    * Did we handle loading states?
    * Did we add logging?
    * Did we clean up temp files?

### Step 4: Verification
1.  **Run Tests:** Execute the relevant test suite (e.g., `uv run pytest`).
2.  **Check Coverage:** Ensure new files have corresponding test files.

### Step 5: The Verdict

Output your report in this format:

> **Verification Report**
>
> **1. Architectural Integrity:** [Pass/Fail]
> * *Redundancy Check:* Did we reinvent the wheel?
> * *Drift Check:* Did we modify files we shouldn't have?
>
> **2. Plan Compliance:** [Pass/Fail]
> * *Completed:* (List major features verified)
> * *Missing/Forgotten:* (List specific items from the plan that are missing in the code)
>
> **3. Edge Case & Gap Analysis:**
> * (List things we likely forgot, e.g., "We implemented the happy path, but there is no try/catch block for the API call.")
>
> **4. Test Results:**
> * (Output of test run)
>
> **Next Actions:**
> (Specific commands to fix the issues, or "Ready to Merge")

## Critical Rules
* **Be Skeptical:** Assume we forgot something.
* **Call out Redundancy:** If we implemented a custom modal when the project uses a UI library, flag it as a generic "Reinvention" failure.
* **Verify Tests Exist:** It is not enough that tests pass; they must actually *cover* the new code.
