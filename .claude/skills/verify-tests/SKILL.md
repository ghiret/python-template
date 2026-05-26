---
name: verify-tests
description: Fast test-quality audit. Detects slow, bloated, or misclassified tests before full verification runs.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Verify Tests: Fast Test-Quality Gate

## Overview

You act as a **Test Quality Auditor**. Your job is to prevent slow or
misclassified tests from blocking execution and verification. This is a fast
audit, not a full test-suite run.

**Trigger:** Run after `/execute` and before `/verify`, especially in
`/ralph-execute`.

Before auditing, read `_shared/testing-conventions.md`.

## Critical Runtime Rule

Do NOT run the full test suite by default. Use static inspection first. Run
targeted tests only when needed, and use explicit timeouts when available.

## The Process

### Step 1: Identify New or Modified Tests

1. Run `git diff --name-only main...HEAD` or the appropriate base branch.
2. Identify changed test files and nearby test configuration.
3. If a plan file was provided, read it to understand expected test coverage.

### Step 2: Static Test Audit

Inspect changed tests for:

- Unit tests that can exceed 60 seconds.
- `sleep`, long timeout, retry, polling, or wall-clock dependent behavior.
- Real network, cloud, database, browser, or filesystem-heavy behavior inside
  unit tests.
- Unbounded loops, unbounded property-based tests, or excessive generated data.
- Large snapshots, huge golden files, or broad fixture setup.
- Integration/e2e/load behavior that is not marked `slow`, `integration`,
  `e2e`, `load`, or equivalent.
- Tests that are placed or named as unit tests but exercise full workflows.

### Step 3: Targeted Runtime Check

Only if static inspection is inconclusive:

1. Run the smallest relevant subset of tests.
2. Use a timeout when available, for example `timeout 60s <test command>` on
   systems that provide `timeout`.
3. Do not trigger known long integration/e2e/load tests unless the user asked
   for them.

### Step 4: Fix Once If Needed

If test quality fails:

1. Fix the test design once.
2. Prefer faster unit-test seams over long sleeps or real services.
3. Mark legitimate long tests as `slow`, `integration`, `e2e`, or equivalent.
4. Re-run this fast audit once.

If it still fails, stop and report the remaining test-quality issues.

### Step 5: Report

Write the test-quality report to
`agent_docs/reports/verify/{plan-slug}-test-quality.html` when a plan is known,
or `agent_docs/reports/verify/test-quality.html` otherwise. Use the shared HTML
report skeleton from `_shared/html-conventions.md`.

Also output one exact marker in the conversation:

```text
TEST QUALITY PASSED
```

or

```text
TEST QUALITY FAILED: {issues}
```

## Critical Rules

- NEVER run the full test suite by default.
- NEVER approve a unit test that can exceed 60 seconds.
- NEVER let integration/e2e/load tests masquerade as unit tests.
- NEVER accept sleeps, real network calls, unbounded generated data, or huge
  fixtures in unit tests without a clear, fast bound.
- ALWAYS keep this audit cheap enough to run before full implementation
  verification.
