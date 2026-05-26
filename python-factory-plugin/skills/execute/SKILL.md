---
name: execute
description: Executes implementation plans autonomously in batches. Runs all tasks to completion without pausing for feedback unless blocked.
disable-model-invocation: true
---

# Executing Plans

## Overview

Load plan, review critically, execute ALL tasks to completion autonomously.

**Core principle:** Autonomous execution — run all tasks without stopping for feedback. The user will interrupt if they need to.

**Announce at start:** "I'm using the execute skill to implement this plan."

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns are **blocking** (cannot proceed without clarification): raise them and stop
4. If concerns are **non-blocking** (minor, can make a reasonable decision): note them and proceed
5. Create tasks and proceed

### Step 2: Execute Batch
**Default: First 3 tasks**

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Run the tests: unit test, integration tests, frontend tests, hypothesis based tests
5. Fix all failing tests
6. Ask yourself, have I tested this enough? Are the tests that I have written good? Are some of them redundant? Can I write better tests? And think hard about how to improve the tests, then implement the results of this thinking.
7. Run the tests: unit test, integration tests, frontend tests, hypothesis based tests
8. Fix all failing tests
9. Ask yourself, have I tested this enough? Are the tests that I have written good? Are some of them redundant? Can I write better tests? And think hard about how to improve the tests, then implement the results of this thinking.
10. Run the tests: unit test, integration tests, frontend tests, hypothesis based tests
11. Fix all failing tests
12. Mark as completed

### Step 3: Continue to Next Batch
**Do NOT stop for feedback.** Immediately proceed to the next batch of tasks.
- Log what was implemented for the summary
- Move to the next 3 tasks
- Repeat until ALL tasks are complete

### Step 4: Complete Development

After all tasks complete and verified:
1. **Final Test Run:** Run the full project test suite to ensure no regressions.
2. **Handover:** Announce: "Implementation complete and verified. Ready for final review."

## When to Stop

**STOP executing ONLY when:**
- Hit an unrecoverable blocker (missing dependency that can't be installed, critical ambiguity)
- Verification fails repeatedly (3+ attempts) on the same issue
- All tasks are complete

**Do NOT stop for:**
- Minor concerns — make a reasonable decision and continue
- Feedback checkpoints — the user will interrupt if needed
- Asking whether to continue — just continue
- Cleanup questions — keep the plan file, don't ask

## Remember
- Run autonomously from start to finish
- Follow plan steps exactly
- Don't skip verifications
- Don't pause for feedback — the user will interrupt if they need to
- Reference skills when plan references them
