---
name: ralph-execute
description: Autonomous execution pipeline. Parses plan phases, executes each via agents (execute → verify → docs → commit), then runs drift review between phases. Usage: /ralph-execute [review-iterations=5] <plan-file>
disable-model-invocation: true
argument-hint: "[review-iterations=5] <plan-file>"
---

# Ralph Execute: Autonomous Implementation Pipeline

Parse arguments:
- If one argument: review_iterations=5, plan_file=$ARGUMENTS[0]
- If two arguments: review_iterations=$ARGUMENTS[0], plan_file=$ARGUMENTS[1]

## MANDATORY COMPLETION RULE

**YOU MUST PROCESS EVERY PHASE in the plan.** Do NOT stop early because "the code looks complete", because "remaining phases are trivial", or for any other reason. The ONLY valid reasons to stop are:
1. All phases in the plan have been processed
2. A verification failure that cannot be fixed (after retry)
3. An unrecoverable error

## Setup

1. Read the plan file and extract all phases by finding `## Phase N: Title` headings.
2. Count the total number of phases (P).
3. Create a top-level task "Ralph Execute: {P} phases from {plan_file}" and set to IN_PROGRESS.
4. Announce: **"=== RALPH EXECUTE: Found {P} phases. Review iterations per phase: {review_iterations} ==="**
5. Do NOT create phase sub-tasks upfront — create them as each phase begins.

## Execution Loop

For each phase i = 1, 2, 3, ..., P (you MUST go in order, one at a time):

### Step A: Execute Phase (via Agent)

1. Create task "Phase {i}/{P}: Execute — {phase_title}" and set to IN_PROGRESS
2. Announce: **"=== PHASE {i} OF {P}: EXECUTE — {phase_title} ==="**
3. Extract the tasks and verification steps for ONLY this phase from the plan
4. Spawn an Agent with subagent_type "general-purpose" and this prompt:

   > You are executing Phase {i} of an implementation plan.
   >
   > Plan file: {plan_file}
   >
   > Read the skill file `.claude/skills/execute/SKILL.md` and follow its process to implement ONLY the following phase:
   >
   > {paste the full phase content here, including tasks and verification subsection}
   >
   > IMPORTANT: Do NOT implement tasks from any other phase. ONLY implement the tasks listed above.
   > When done, announce "Phase {i} execution complete."

5. Wait for the agent to complete
6. Update task to COMPLETED

### Step B: Verify Implementation (via Agent)

7. Create task "Phase {i}/{P}: Verify implementation" and set to IN_PROGRESS
8. Announce: **"=== PHASE {i} OF {P}: VERIFY ==="**
9. Spawn an Agent with subagent_type "general-purpose" and this prompt:

   > You are verifying the implementation of Phase {i} of a plan.
   >
   > Plan file: {plan_file}
   >
   > Read the skill file `.claude/skills/verify/SKILL.md` and execute its full verification process.
   > Focus on whether Phase {i} was implemented correctly, but also check for regressions in earlier phases.
   >
   > If verification FAILS:
   > - Attempt to fix the issues you find
   > - Re-run the verification once more
   > - Report the final result clearly: "VERIFICATION PASSED" or "VERIFICATION FAILED: {issues}"

10. Wait for the agent to complete
11. Parse the result:
    - If **PASSED**: Update task to COMPLETED, proceed
    - If **FAILED after retry**: Update task to FAILED, update top-level task to FAILED, STOP and report: "Phase {i} verification failed after retry. Issues: {list}"
12. Update task to COMPLETED

### Step C: Documentation Pipeline (via Agents)

This step has 4 sub-steps. The review runs always; the fixes run only if the review flags issues.

#### C1: Review Docs (via Agent — always runs)

13. Create task "Phase {i}/{P}: Review docs" and set to IN_PROGRESS
14. Announce: **"=== PHASE {i} OF {P}: REVIEW DOCS ==="**
15. Spawn an Agent with subagent_type "general-purpose" and this prompt:

    > You are reviewing documentation after Phase {i} of an implementation.
    >
    > Read the skill file `.claude/skills/review-docs/SKILL.md` and execute its full drift analysis.
    > Output the Documentation Drift Report with tagged actions: [FIX-DOCS], [GENERATE-DIAGRAMS], [GENERATE-IMAGES].

16. Wait for the agent to complete
17. Save the drift report output for the next sub-steps
18. Update task to COMPLETED

#### C2: Fix Docs (via Agent — only if [FIX-DOCS] items found)

19. If the drift report contains **[FIX-DOCS]** items:
    - Create task "Phase {i}/{P}: Fix docs" and set to IN_PROGRESS
    - Spawn an Agent with subagent_type "general-purpose" and this prompt:

      > You are fixing text documentation after Phase {i} of an implementation.
      >
      > Read the skill file `.claude/skills/fix-docs/SKILL.md` and apply fixes for these findings:
      >
      > {paste the [FIX-DOCS] items from the drift report}

    - Wait for the agent to complete
    - Update task to COMPLETED

#### C3: Generate Diagrams (via Agent — only if [GENERATE-DIAGRAMS] items found)

20. If the drift report contains **[GENERATE-DIAGRAMS]** items:
    - Create task "Phase {i}/{P}: Generate diagrams" and set to IN_PROGRESS
    - Spawn an Agent with subagent_type "general-purpose" and this prompt:

      > You are updating architecture diagrams after Phase {i} of an implementation.
      >
      > Read the skill file `.claude/skills/generate-diagrams/SKILL.md` and update diagrams for these findings:
      >
      > {paste the [GENERATE-DIAGRAMS] items from the drift report}

    - Wait for the agent to complete
    - Update task to COMPLETED

#### C4: Generate Images (via Agent — only if [GENERATE-IMAGES] items found)

21. If the drift report contains **[GENERATE-IMAGES]** items:
    - Create task "Phase {i}/{P}: Generate images" and set to IN_PROGRESS
    - Spawn an Agent with subagent_type "general-purpose" and this prompt:

      > You are generating AI documentation images after Phase {i} of an implementation.
      >
      > Read the skill file `.claude/skills/generate-images/SKILL.md` and generate images for these findings:
      >
      > {paste the [GENERATE-IMAGES] items from the drift report}

    - Wait for the agent to complete
    - Update task to COMPLETED

Documentation issues from C2-C4 are warnings, not blockers — note them but proceed to Step D.

### Step D: Pre-commit & Commit

18. Create task "Phase {i}/{P}: Pre-commit & commit" and set to IN_PROGRESS
19. Announce: **"=== PHASE {i} OF {P}: COMMIT ==="**
20. Run: `uv run pre-commit run --all-files`
    - If pre-commit modifies files, run it again to confirm clean
    - If pre-commit fails on the second run, STOP and report
21. Stage changed files safely:
    - Run `git diff --name-only` and `git ls-files --others --exclude-standard` to list changes
    - Review the list — NEVER stage `.env`, credentials, or large binaries
    - Stage files by name: `git add <file1> <file2> ...`
22. Create a semantic commit:
    - Read the git diff to understand what changed
    - Use conventional commit format: `feat:`, `fix:`, `refactor:`, etc.
    - Include `Phase {i}/{P}: {phase_title}` in the commit body
    - End with `Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>`
23. Run: `git commit -m "<message>"` using a HEREDOC for the message
24. Update task to COMPLETED

### Step E: Drift Review (via /ralph-review)

25. Create task "Phase {i}/{P}: Drift review ({review_iterations} iterations)" and set to IN_PROGRESS
26. Announce: **"=== PHASE {i} OF {P}: DRIFT REVIEW ({review_iterations} iterations) ==="**
27. Read `.claude/skills/ralph-review/SKILL.md` and execute its full review process with {review_iterations} iterations on {plan_file}
    - This detects whether the plan still makes sense given what was just implemented
    - The plan may be updated if drift is detected
28. Wait for all review iterations to complete
29. Update task to COMPLETED

### Step F: Re-read Plan & Continue

30. Re-read {plan_file} — it may have been modified by the drift review
31. Re-extract the remaining phases (the phase structure may have shifted)
32. If this is the LAST phase (i == P):
    - Update top-level task to COMPLETED
    - Announce: **"=== ALL {P} PHASES COMPLETE ==="**
    - Output the final summary table (see below)
    - List all commits created during this run
    - **STOP — all phases done**
33. Otherwise: **YOU MUST proceed to phase {i+1}. Do NOT stop here.**

## Summary Table

After completion (or failure), output:

```
| Phase | Title              | Execute | Verify | Docs Review | Fix Docs | Diagrams | Images | Commit | Drift Review        |
|-------|--------------------|---------|--------|-------------|----------|----------|--------|--------|---------------------|
| 1/P   | Set up models      | Done    | PASSED | 2 issues    | Fixed    | Skipped  | Skipped| abc123 | APPROVED (iter 2)   |
| 2/P   | API endpoints      | Done    | PASSED | Clean       | Skipped  | Updated  | Skipped| def456 | REQUEST CHANGES (5) |
| 3/P   | ...                | ...     | ...    | ...         | ...      | ...      | ...    | ...    | ...                 |
```

## Important Rules

**COMPLETION IS NON-NEGOTIABLE.** Every phase in the plan MUST be processed. The user expects all phases to run.

- NEVER skip a phase — every phase must go through Steps A through F
- NEVER skip verification — always verify after execute
- NEVER skip the drift review — it catches plan drift between phases
- NEVER commit without running pre-commit first
- NEVER combine phases — each phase is a separate execute+verify+commit+review cycle
- If verification fails twice, STOP — don't force through broken code
- Always announce phase transitions prominently: **"=== PHASE {i} OF {P}: ... ==="**
- Always use semantic commit messages based on actual changes
- If an agent returns an error, stop and report it clearly
- The drift review may modify the plan — always re-read the plan after the review step
