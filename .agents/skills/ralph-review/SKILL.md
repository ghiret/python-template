---
name: ralph-review
description: Autonomous review loop. Spawns agents for /review-plan and /fix-plan up to N times until the plan is approved. Usage: /ralph-review [iterations] <plan-file>
disable-model-invocation: true
argument-hint: "[iterations=5] <plan-file>"
---

# Ralph Review: Autonomous Plan Review Loop

Parse arguments:
- If one argument: iterations=5, plan_file=$ARGUMENTS[0]
- If two arguments: iterations=$ARGUMENTS[0], plan_file=$ARGUMENTS[1]

## MANDATORY COMPLETION RULE

**YOU MUST COMPLETE EVERY SINGLE ITERATION from 1 to N.** The ONLY exception is an explicit APPROVED verdict from the review agent. Do NOT stop early because the plan "looks good", because changes are "minor", because you think further iterations are "unnecessary", or for any other reason. If the verdict is REQUEST CHANGES, you MUST continue to the next iteration — no exceptions.

After the LAST iteration completes, output a summary table like this:

```
| Iteration | Verdict          | Changes Made |
|-----------|------------------|--------------|
| 1 of 5    | REQUEST CHANGES  | Yes          |
| 2 of 5    | REQUEST CHANGES  | Yes          |
| 3 of 5    | APPROVED         | N/A (stopped)|
```

## Setup

1. Create a top-level task "Ralph Review: {N} iterations on {plan_file}" and set to IN_PROGRESS.
2. Do NOT create iteration sub-tasks upfront. Create each iteration's task as it begins.

## Execution Loop

For each iteration i = 1, 2, 3, ..., N (you MUST go in order, one at a time):

### Step A: Review (via Agent)
1. Create task "Review iteration {i} of {N}" and set to IN_PROGRESS
2. Announce: **"=== REVIEW ITERATION {i} OF {N} ==="**
3. Spawn an Agent with subagent_type "general-purpose" and this prompt:

   > You are reviewing an implementation plan (iteration {i} of {N}).
   >
   > Plan file: {plan_file}
   >
   > Read the skill file `.claude/skills/review-plan/SKILL.md` and execute its FULL review process on the plan file.
   >
   > You MUST output the complete review report with the exact verdict format:
   > **Review Status:** APPROVED
   > or
   > **Review Status:** REQUEST CHANGES
   >
   > Do not skip any of the four inspection points (Redundancy, Architecture, Testability, Phase Structure).

4. Wait for the agent to complete
5. Read the agent's output carefully and extract the verdict

### Step B: Check Verdict
6. Parse the Review Status from the agent's output:
   - If **APPROVED**:
     - Update task to COMPLETED with note "APPROVED on iteration {i}"
     - Update top-level task to COMPLETED
     - Announce: "Plan approved after {i} iteration(s). Ready for /ralph-execute or /execute."
     - Output the summary table
     - **STOP — plan is approved**
   - If **REQUEST CHANGES**:
     - Update task to COMPLETED with note "REQUEST CHANGES"
     - Proceed to Step C

### Step C: Fix (via Agent)
7. Spawn an Agent with subagent_type "general-purpose" and this prompt:

   > You are fixing an implementation plan based on review feedback (iteration {i} of {N}).
   >
   > Plan file: {plan_file}
   >
   > The review produced these findings:
   > {paste the full review report from Step A here}
   >
   > Read the skill file `.claude/skills/fix-plan/SKILL.md` and execute its fix process on the plan file.
   > Apply ALL recommended changes from the review.
   > When done, announce what was changed.

8. Wait for the agent to complete
9. Verify the plan file was modified (check git diff on the file)
10. If this is the LAST iteration (i == N):
    - Update top-level task to COMPLETED with note "Reached max iterations"
    - Announce: "Reached maximum iterations ({N}). Plan still has requested changes."
    - Output the summary table
    - **STOP — max iterations reached**
11. Otherwise: **YOU MUST proceed to iteration {i+1}. Do NOT stop here.**

## Important Rules

**COMPLETION IS NON-NEGOTIABLE.** Re-read the MANDATORY COMPLETION RULE above before each iteration. The user is paying for {N} iterations and expects all of them to run.

- NEVER skip an iteration — every iteration must execute Steps A, B, and C (unless APPROVED)
- NEVER skip the review step — always spawn the review agent and get fresh feedback
- NEVER stop early because "the plan looks fine" or "changes are minimal" — only APPROVED stops the loop
- NEVER proceed past a STOP point
- NEVER batch or combine iterations — each one is a separate review+fix cycle with separate agents
- If an agent returns an error, stop and report the error clearly
- Always announce the iteration number prominently: **"=== REVIEW ITERATION {i} OF {N} ==="**
- After APPROVED, do NOT run the fix agent
- Always pass the FULL review report to the fix agent so it has context
