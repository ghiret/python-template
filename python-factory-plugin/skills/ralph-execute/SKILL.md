---
name: ralph-execute
description: Autonomous execution pipeline. Runs /execute, /verify, /verify-docs, pre-commit, and commits per phase. Usage: /ralph-execute [max-phases=5] <plan-file>
disable-model-invocation: true
argument-hint: "[max-phases=5] <plan-file>"
---

# Ralph Execute: Autonomous Implementation Pipeline

Parse arguments:
- If one argument: max_phases=5, plan_file=$ARGUMENTS[0]
- If two arguments: max_phases=$ARGUMENTS[0], plan_file=$ARGUMENTS[1]

## Setup

Read the plan file to understand the scope. Identify the major phases/batches of work.

Do NOT create all tasks upfront — create tasks dynamically as each phase starts, since the number of phases depends on the plan's scope and how the execute process batches the work.

## Execution Loop

For each phase (1 to max_phases):

### Step A: Execute
1. Create task "Phase {i}: Execute batch" and set to IN_PROGRESS
2. Announce: "Starting phase {i} of {max_phases}"
3. Read `.claude/skills/execute/SKILL.md` and execute its process on {plan_file}
   - The execute process runs in batches of 3 tasks by default
   - After each batch it reports "Ready for feedback."
   - When you see "Ready for feedback", review what was implemented, then provide "continue" to trigger the next batch
   - Keep running batches within this phase until either:
     a. The execute process says "Implementation complete and verified. Ready for final review." — this is the last phase
     b. A natural phase boundary is reached (all related tasks in a group are done)
4. Update task to COMPLETED

### Step B: Verify Implementation
5. Create task "Phase {i}: Verify implementation" and set to IN_PROGRESS
6. Read `.claude/skills/verify/SKILL.md` and execute its full verification process
7. Parse the Verification Report:
   - If **all checks pass**: Update task to COMPLETED, proceed
   - If **failures found**:
     - Attempt to fix the issues identified in the report
     - Re-execute the verification process from `.claude/skills/verify/SKILL.md` once more
     - If still failing: STOP and report "Phase {i} verification failed. Issues: {list}"
8. Update task to COMPLETED

### Step C: Verify Documentation
9. Create task "Phase {i}: Verify documentation" and set to IN_PROGRESS
10. Read `.claude/skills/verify-docs/SKILL.md` and execute its documentation verification process
11. Review the Documentation & Visuals Report
12. Update task to COMPLETED
    (Documentation issues are warnings, not blockers — note them but proceed)

### Step D: Pre-commit & Commit
13. Create task "Phase {i}: Pre-commit & commit" and set to IN_PROGRESS
14. Run: `uv run pre-commit run --all-files`
    - If pre-commit modifies files, run it again to confirm clean
    - If pre-commit fails on the second run, STOP and report
15. Stage changed files safely:
    - Run `git diff --name-only` and `git ls-files --others --exclude-standard` to list changes
    - Review the list — NEVER stage `.env`, credentials, or large binaries
    - Stage files by name: `git add <file1> <file2> ...`
    - If unsure about a file, skip it and note it in the commit message
16. Create a semantic commit message:
    - Read the git diff to understand what changed
    - Use conventional commit format: `feat:`, `fix:`, `refactor:`, etc.
    - Include "Phase {i}/{max_phases}" in the commit body
    - End with `Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>`
17. Run: `git commit -m "<message>"`
18. Update task to COMPLETED

### Step E: Check Completion
19. If the execute process indicated all plan tasks are complete:
    - Announce: "All phases complete. {total_phases} commits created."
    - List all commits created during this run
    - **STOP HERE**
20. Otherwise: proceed to next phase

## Important Rules
- NEVER skip verification steps — always run verify after execute
- NEVER commit without running pre-commit first
- If verification fails twice, STOP — don't force through
- Always use semantic commit messages based on actual changes
- Announce phase transitions clearly: "Phase 2 of 5: Starting execution"
- At the end, show a summary table of all phases, tasks, and commit hashes
- If max_phases is reached but plan isn't complete, announce remaining work
