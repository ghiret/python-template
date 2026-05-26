---
name: ralph-execute
description: "Autonomous execution pipeline. Parses plan phases, executes selected phases via agents (execute → verify → docs → commit → drift review). Usage: /ralph-execute [review-iterations=5] [phase=N|phases=N-M|phases=N,M] plan-file"
metadata:
  argument-hint: "[review-iterations=5] [phase=N|phases=N-M|phases=N,M] <plan-file>"
---

# Ralph Execute: Autonomous Implementation Pipeline

Parse arguments:
- If one argument: review_iterations=5, plan_file=$ARGUMENTS[0]
- If two arguments: review_iterations=$ARGUMENTS[0], plan_file=$ARGUMENTS[1]
- Phase selection is optional:
  - `phase=N` may appear before the plan file: `/ralph-execute phase=2 agent_docs/plans/my-plan.html`
  - `phase N` may appear before the plan file: `/ralph-execute phase 2 agent_docs/plans/my-plan.html`
  - `phases=N-M` runs an inclusive range: `/ralph-execute phases=2-4 agent_docs/plans/my-plan.html`
  - `phases=N,M,K` runs an explicit ordered list: `/ralph-execute phases=1,3 agent_docs/plans/my-plan.html`
  - A review iteration count may still come first: `/ralph-execute 3 phase=2 agent_docs/plans/my-plan.html`
- If no phase selector is provided, selected_phases=ALL.

## Skill Path Resolution

When reading companion skills, prefer `.agents/skills/<name>/SKILL.md` if it exists
(Codex layout). Otherwise use `.claude/skills/<name>/SKILL.md` (Claude layout).

Also read the shared conventions before setup:
- `_shared/html-conventions.md` for HTML plan parsing and report artifact locations
- `_shared/testing-conventions.md` for test speed budgets enforced by execute and verify

## MANDATORY COMPLETION RULE

**YOU MUST PROCESS THE REQUESTED SCOPE IN STRICT PHASE CYCLES.**

- If selected_phases=ALL, process every phase in the plan. Do NOT stop early because "the code looks complete", because "remaining phases are trivial", or for any other reason.
- If selected_phases is a subset, process exactly those phases and no other phases.
- For each selected phase, run the complete cycle in this order: Execute → Verify → Docs → Commit → Drift Review → Re-read Plan.
- Execute and Verify are deliberately separate repeated passes for every selected phase. LLM agents are fallible: the execute agent can miss tasks, overreach, or introduce regressions, so the verify agent MUST independently check the phase before docs, commit, or drift review proceed.
- Do NOT run docs, commit, or drift review for a phase until that same phase has passed execution and verification.
- Do NOT advance to the next selected phase until the current phase has completed the full cycle, including drift review.

The ONLY valid reasons to stop are:
1. The requested scope has been processed
2. A verification failure that cannot be fixed (after retry)
3. An unrecoverable error

## Setup

1. Read the plan file and extract all phases:
   - For `.html` plans, extract phases from `<section data-phase="N" data-title="...">`, tasks from `<ul class="tasks"><li>...`, and verification from `<section class="verification">`.
   - For `.md` plans, extract phases by finding `## Phase N: Title` headings, `- [ ]` tasks, and `### Verification` subsections.
2. Count the total number of phases (P).
3. Resolve the requested scope:
   - If no selector is provided: selected_phases = [1, 2, ..., P]
   - If `phase=N` or `phase N` is provided: selected_phases = [N]
   - If `phases=N-M` is provided: selected_phases = [N, N+1, ..., M]
   - If `phases=N,M,K` is provided: selected_phases = [N, M, K] in the requested order
   - Reject duplicate, missing, non-numeric, descending range, or out-of-range phase selectors. STOP and report the valid phase range and phase titles.
4. Create a top-level task:
   - All phases: "Ralph Execute: {P} phases from {plan_file}"
   - Selected phases: "Ralph Execute: phases {selected_phases} of {P} from {plan_file}"
5. Announce one of:
   - **"=== RALPH EXECUTE: Found {P} phases. Processing ALL phases. Review iterations per phase: {review_iterations} ==="**
   - **"=== RALPH EXECUTE: Found {P} phases. Processing ONLY selected phases {selected_phases}. Review iterations per phase: {review_iterations} ==="**
6. Do NOT create phase sub-tasks upfront — create them as each phase begins.

## Execution Loop

For each phase i in selected_phases (you MUST go in order, one at a time):

Every selected phase MUST repeat Step A and Step B as distinct passes:
1. Execute Phase i with the execute companion skill.
2. Verify Phase i with the verify companion skill.
3. Only after verification passes, continue to docs, commit, drift review, and the next selected phase.

### Step A: Execute Phase (via Agent)

1. Create task "Phase {i}/{P}: Execute — {phase_title}" and set to IN_PROGRESS
2. Announce: **"=== PHASE {i} OF {P}: EXECUTE — {phase_title} ==="**
3. Extract the tasks and verification steps for ONLY this phase from the plan
4. Spawn an Agent with subagent_type "general-purpose" and this prompt:

   > You are executing Phase {i} of an implementation plan.
   >
   > Plan file: {plan_file}
   >
   > Read the `execute` companion skill using the Skill Path Resolution rule above and follow its process to implement ONLY the following phase:
   >
   > {paste the full phase content here, including tasks and verification subsection}
   >
   > IMPORTANT:
   > - The source plan may be HTML or Markdown. Preserve and follow the parsed phase content exactly.
   > - Do NOT implement tasks from any other phase. ONLY implement the tasks listed above.
   > - Run AUTONOMOUSLY — do NOT stop for feedback or ask for confirmation. Execute all tasks to completion.
   > - Keep tests bounded and fast. Do NOT add unit tests that can exceed 60 seconds; mark long integration/e2e tests explicitly.
   > - Only stop if you hit an unrecoverable blocker (3+ failed attempts on the same issue).
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
   > Read the `verify` companion skill using the Skill Path Resolution rule above and execute its full verification process.
   > Focus on whether Phase {i} was implemented correctly, but also check for regressions in earlier phases.
   > Write the verification report artifact under `agent_docs/reports/verify/` and include a stable `VERIFICATION PASSED` or `VERIFICATION FAILED` marker.
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
    > Read the `review-docs` companion skill using the Skill Path Resolution rule above and execute its full drift analysis.
    > Write the Documentation Drift Report artifact under `agent_docs/reports/drift/` and include tagged actions: [FIX-DOCS], [GENERATE-DIAGRAMS], [GENERATE-IMAGES].

16. Wait for the agent to complete
17. Save the drift report output and artifact path from `agent_docs/reports/drift/` for the next sub-steps
18. Update task to COMPLETED

#### C2: Fix Docs (via Agent — only if [FIX-DOCS] items found)

19. If the drift report contains **[FIX-DOCS]** items:
    - Create task "Phase {i}/{P}: Fix docs" and set to IN_PROGRESS
    - Spawn an Agent with subagent_type "general-purpose" and this prompt:

      > You are fixing text documentation after Phase {i} of an implementation.
      >
      > Read the `fix-docs` companion skill using the Skill Path Resolution rule above and apply fixes for these findings:
      >
      > {paste the [FIX-DOCS] items from the drift report}
      >
      > If findings are not available in the conversation, read the latest drift report from `agent_docs/reports/drift/`.

    - Wait for the agent to complete
    - Update task to COMPLETED

#### C3: Generate Diagrams (via Agent — only if [GENERATE-DIAGRAMS] items found)

20. If the drift report contains **[GENERATE-DIAGRAMS]** items:
    - Create task "Phase {i}/{P}: Generate diagrams" and set to IN_PROGRESS
    - Spawn an Agent with subagent_type "general-purpose" and this prompt:

      > You are updating architecture diagrams after Phase {i} of an implementation.
      >
      > Read the `generate-diagrams` companion skill using the Skill Path Resolution rule above and update diagrams for these findings:
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
      > Read the `generate-images` companion skill using the Skill Path Resolution rule above and generate images for these findings:
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
    - If selected_phases is not ALL, include `Selected-phase Ralph run: requested phases {selected_phases} of {P}` in the commit body
    - End with `Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>`
23. Run: `git commit -m "<message>"` using a HEREDOC for the message
24. Update task to COMPLETED

### Step E: Drift Review (via /ralph-review)

25. Create task "Phase {i}/{P}: Drift review ({review_iterations} iterations)" and set to IN_PROGRESS
26. Announce: **"=== PHASE {i} OF {P}: DRIFT REVIEW ({review_iterations} iterations) ==="**
27. Read the `ralph-review` companion skill using the Skill Path Resolution rule above and execute its full review process with {review_iterations} iterations on {plan_file}
    - This detects whether the plan still makes sense given what was just implemented
    - The plan may be updated if drift is detected
    - Review artifacts should be written under `agent_docs/reports/reviews/`
28. Wait for all review iterations to complete
29. Update task to COMPLETED

### Step F: Re-read Plan & Continue

30. Re-read {plan_file} — it may have been modified by the drift review
31. Re-extract the remaining phases (the phase structure may have shifted)
32. If selected_phases is not ALL and this is the LAST selected phase:
    - Update top-level task to COMPLETED
    - Announce: **"=== REQUESTED PHASES {selected_phases} COMPLETE ==="**
    - Output the final summary table for the requested phase(s)
    - List all commits created during this run
    - **STOP — requested selected phases done**
33. If this is the LAST phase (i == P):
    - Update top-level task to COMPLETED
    - Announce: **"=== ALL {P} PHASES COMPLETE ==="**
    - Output the final summary table (see below)
    - List all commits created during this run
    - **STOP — all phases done**
34. Otherwise: **YOU MUST proceed to the next selected phase. Do NOT stop here.**

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

**COMPLETION IS NON-NEGOTIABLE.** The requested scope MUST be processed. Without a phase selector, every phase in the plan MUST be processed. With a phase selector, exactly the selected phase(s) MUST be processed.

- NEVER skip a requested phase — each selected phase must go through Steps A through F
- NEVER process unrequested phases in selected-phase mode
- NEVER reorder the per-phase cycle: execute and verify first, then docs, then commit, then drift review
- NEVER treat execution alone as sufficient — verification is a separate pass because LLM agents are fallible
- NEVER skip verification — always verify after execute
- NEVER skip the drift review — it catches plan drift between phases
- NEVER ignore report artifacts — verification, docs drift, and plan review reports should live under `agent_docs/reports/`
- NEVER commit without running pre-commit first
- NEVER combine phases — each phase is a separate execute+verify+commit+review cycle
- If verification fails twice, STOP — don't force through broken code
- Always announce phase transitions prominently: **"=== PHASE {i} OF {P}: ... ==="**
- Always use semantic commit messages based on actual changes
- If an agent returns an error, stop and report it clearly
- The drift review may modify the plan — always re-read the plan after the review step
