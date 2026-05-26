# AGENTS.md

## First Time Setup

If this is a freshly cloned template, run `$init-project` to configure project
metadata, license, directory structure, and remote settings.

## Workspace Rules

- Work only inside the current project root.
- Store implementation plans in `agent_docs/plans/`.
- Store generated reports under `agent_docs/reports/`.
- Store scratch, research, imported docs, and temporary references in
  `agent_docs/`.
- `agent_docs/` and `external_docs/` are untracked workspaces by default.

## Skill Workflow

Use this lifecycle for feature work:

1. **Architecture**: Create an HTML plan in `agent_docs/plans/` following
   `.claude/skills/_shared/html-conventions.md`. Markdown plans still work.
   Run `$review-plan`.
2. **Execution**: Implement the plan in batches. Run `$execute`.
3. **Test Quality**: Audit tests before full verification. Run `$verify-tests`.
4. **Quality Assurance**: Verify the branch before merging. Run `$verify`.
5. **Documentation**: Audit docs with `$review-docs`, then apply findings with
   `$fix-docs`, `$generate-diagrams`, or `$generate-images`.

For autonomous development, use `$ralph-review` followed by `$ralph-execute`.

## Artifact And Testing Conventions

- HTML is the preferred artifact format for plans and reports.
- Markdown remains supported for existing workflows.
- Unit tests should be fast and deterministic.
- No unit test may take longer than 60 seconds.
- Long integration, e2e, load, or soak tests must be marked and kept separate
  from the fast unit-test path.

## Coding Standards

- Use `uv` for Python dependency management.
- Use `pytest` for tests.
- Use `ruff` for linting and formatting.
- Use type hints for function signatures.
- Check `pyproject.toml` before adding dependencies.
- Run `uv run pre-commit run --all-files` before committing.

## Useful Commands

```bash
uv run pytest
uv run pytest -m "not slow"
uv run pre-commit run --all-files
uv run mkdocs build
```

## Codex Notes

`.agents/skills/` keeps Codex-compatible copies of the `.claude/skills/`
skill bodies. If a skill changes, update both copies and run the skill
frontmatter tests to verify they stay synchronized.
