# Testing Budget Conventions

These conventions keep generated test suites useful without letting them block
development. Tests should increase confidence quickly. Slow tests are allowed
only when they are intentionally classified as integration, end-to-end, load, or
soak tests.

## Test Categories

- Unit tests: isolated, deterministic tests for a function, class, component, or
  small module. They must not depend on network services, real cloud resources,
  long sleeps, large generated datasets, or wall-clock timing.
- Integration tests: tests that cross process, database, filesystem, service, or
  framework boundaries. They may be slower, but must be marked or named so they
  can be excluded from the fast default loop.
- End-to-end and load tests: long-running tests that exercise full workflows,
  browsers, external services, concurrency, volume, or soak behavior. These must
  never be disguised as unit tests.

## Speed Budgets

- Unit test target: under 1 second per test.
- Unit test hard ceiling: no individual unit test may take more than 60 seconds.
- Fast default suite target: complete in about 60 seconds for normal feature work
  unless the repository already documents a different target.
- Long tests over 60 seconds must be explicitly justified, marked as
  `slow`, `integration`, `e2e`, `load`, or equivalent, and kept out of the fast
  unit-test path.

## Design Rules

- Prefer small fixtures over large generated datasets.
- Avoid sleeps. Use fake clocks, polling with tight timeouts, or dependency
  injection.
- Avoid real network calls. Use fakes, mocks, local test servers, or recorded
  fixtures.
- Bound property-based tests with sensible example counts and deadlines.
- Do not add broad snapshot tests or huge golden files unless they are clearly
  valuable and cheap to run.
- If a test is slow because production code is hard to isolate, improve the
  seam in production code instead of making a slow unit test.

## Verification Rules

When reviewing or verifying tests:

- Flag any unit test that can exceed 60 seconds.
- Flag any test that performs integration/e2e work but is named or placed as a
  unit test.
- Flag unbounded loops, sleeps, large randomized inputs, real network calls, and
  large filesystem scans in unit tests.
- Require slow tests to be marked and runnable separately from the fast default
  suite.
- Treat test bloat as a correctness issue: a passing but impractically slow test
  suite is not ready.
