---
paths: ["tests/**"]
---

# Test Conventions
- Use pytest fixtures for shared setup; avoid `setUp`/`tearDown` classes
- Use `@pytest.mark.parametrize` for data-driven tests
- Use `hypothesis` for property-based tests on pure functions
- Test names: `test_<function>_<scenario>_<expected_result>`
- Mark slow tests with `@pytest.mark.slow`
- Mark integration tests with `@pytest.mark.integration`
- Never mock the database or file system unless testing external API boundaries
- Always assert specific values, not just truthiness
