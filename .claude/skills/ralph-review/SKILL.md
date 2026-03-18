---
name: ralph-review
description: Autonomous review loop. Runs /review-plan and /fix-plan up to N times until the plan is approved. Usage: /ralph-review [iterations] <plan-file>
disable-model-invocation: true
argument-hint: "[iterations=5] <plan-file>"
---

# Ralph Review: Autonomous Plan Review Loop

Parse arguments:
- If one argument: iterations=5, plan_file=$ARGUMENTS[0]
- If two arguments: iterations=$ARGUMENTS[0], plan_file=$ARGUMENTS[1]

## Setup

Do NOT create all tasks upfront. Create each iteration's task as it begins.

## Execution Loop

For each iteration (1 to N):

### Step A: Review
1. Create task "Review iteration {i} of {N}" and set to IN_PROGRESS
2. Announce: "Starting review iteration {i} of {N}"
3. Read `.claude/skills/review-plan/SKILL.md` and execute its full review process on {plan_file}
4. Read the verdict output carefully

### Step B: Check Verdict
5. Parse the Review Status from the output:
   - If **APPROVED**:
     - Update task to COMPLETED with note "APPROVED"
     - Announce: "Plan approved after {i} iteration(s). Ready for /ralph-execute or /execute."
     - **STOP HERE**
   - If **REQUEST CHANGES**:
     - Update task to COMPLETED with note "REQUEST CHANGES"
     - Proceed to Step C

### Step C: Fix
6. Read `.claude/skills/fix-plan/SKILL.md` and execute its fix process on {plan_file}
7. Verify the plan file was modified (check git diff on the file)
8. If this is the last iteration:
   - Announce: "Reached maximum iterations ({N}). Plan still has issues. Review the latest feedback and decide whether to run another /ralph-review cycle or proceed manually."
   - **STOP HERE**
9. Otherwise: proceed to next iteration

## Important Rules
- NEVER skip the review step — always get fresh feedback before fixing
- NEVER proceed past a STOP point
- If the review or fix process errors, stop and report the error
- Always announce the iteration number: "Starting review iteration 2 of 5"
- After APPROVED, do NOT run the fix process
