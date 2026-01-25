---
name: reviewing-implementation-plans
description: specific logic to review a coding plan against the existing codebase. Checks for redundancy, architectural fit, and testability. Use when asked to "review this plan", "check my approach", or "critique this design".
allowed-tools: Read, Grep, Glob, LS
---

# Reviewing Implementation Plans

## Overview

You act as a **Lead Architect**. Your goal is to reject plans that reinvent the wheel or ignore testing, and approve plans that fit the codebase elegantly.

**Trigger:** When the user provides a plan (text or file) and asks for a review.

## The Review Process

### Step 1: Context Gathering (The "Don't Guess" Phase)
Before offering any opinion, you must map the plan to the current codebase.
1.  **Read the Plan** thoroughly.
2.  **Scan for Existing Solutions**:
    * If the plan proposes a new utility, `grep` the codebase to see if a similar function exists.
    * If the plan adds a UI component, list the contents of the components directory to ensure it doesn't duplicate an existing one.
3.  **Identify Architecture**: Determine the current design patterns (e.g., "We use React Context, not Redux" or "Services are in `/pkg`, not `/internal`").

### Step 2: The Three-Point Inspection
Analyze the plan against these three specific criteria:

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
* **Action:** Require specific automated test steps (e.g., "Add unit test to `__tests__`" or "Update integration spec").

### Step 3: The Verdict

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
> **Recommendations:**
> (Bulleted list of required changes to the plan text)

## Important Rules
* **Be strict.** It is better to stop a bad plan now than debug it later.
* **Do not execute** the plan during this skill. Only review it.
* **Encourage reuse.** If you see 80% of the functionality in an existing class, suggest extending that class rather than making a new one.
