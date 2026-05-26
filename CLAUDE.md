# CLAUDE.md

## FIRST TIME SETUP
If this is a freshly cloned template, run `/init-project` to configure:
- Project name, description, and author
- License selection
- Directory structure setup
- Git remote configuration

## DEVCONTAINER PERSISTENCE RULES
**CRITICAL:** This environment is ephemeral. To prevent data loss:
1. **Work Directory:** ONLY write files inside the current project root (`.`).
2. **No Global Paths:** DO NOT write to `~`, `/tmp`, or `/var`.
3. **Plan Storage:** Store all implementation plans in `./agent_docs/plans/`.
4. **Scratchpads:** Store thought processes/checklists in `./docs/scratchpads/`.
5. **Agent Dumps:** Use `./agent_docs/` for research, API docs, or temporary references (untracked).

## SKILL WORKFLOW (The "Software Factory")
You must adhere to this lifecycle for every feature request:

1. **ARCHITECTURE** — Create a markdown plan in `./agent_docs/plans/`. Run `/review-plan` to check against existing code.
2. **EXECUTION** — Implement the plan in batches. Run `/execute`.
3. **QUALITY ASSURANCE** — Verify the branch before merging. Run `/verify`.
4. **DOCUMENTATION** — Audit docs with `/review-docs`, then run `/fix-docs`, `/generate-diagrams`, or `/generate-images` as needed.

## CODING STANDARDS
- **Package Manager:** Use `uv` for all Python dependency management.
- **Linting/Formatting:** Use `ruff` (configured in pyproject.toml). Auto-formatted by PostToolUse hook.
- **Testing:** Code without tests is incomplete. Use `pytest`.
- **Documentation:** Use Google-style docstrings. Docs are auto-generated with MkDocs.
- **Dependencies:** Check `pyproject.toml` before adding new libs. Use `uv add <package>`.
- **Git:** Use `gh` CLI for PRs and Issues.
- **Type Hints:** Use type hints for all function signatures.

## USEFUL COMMANDS
```bash
uv run pytest --cov --cov-report=html  # Generate HTML coverage report
uv run pytest -m "not slow"            # Skip slow tests
uv run pre-commit run --all-files      # Run all hooks
uv run mkdocs serve                    # Serve docs locally (hot reload)
uv run mkdocs build                    # Build static docs
```

## CONTEXT MANAGEMENT
When compacting, always preserve:
- The list of modified files
- Any test commands that were run and their results
- The current phase of the skill workflow (if active)

## PATH-SPECIFIC RULES
Additional coding rules are in `.claude/rules/` and load automatically when working in matching directories.
