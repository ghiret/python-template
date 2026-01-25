# CLAUDE.md

## 🚀 FIRST TIME SETUP
If this is a freshly cloned template, run the `initialize-project` command to configure:
- Project name, description, and author
- License selection
- Directory structure setup
- Git remote configuration

## ⚠️ DEVCONTAINER PERSISTENCE RULES
**CRITICAL:** This environment is ephemeral. To prevent data loss:
1. **Work Directory:** ONLY write files inside the current project root (`.`).
2. **No Global Paths:** DO NOT write to `~`, `/tmp`, or `/var`.
3. **Plan Storage:** Store all implementation plans in `./plans/`.
4. **Scratchpads:** Store thought processes/checklists in `./docs/scratchpads/`.
5. **Agent Dumps:** Use `./agent_docs/` for research, API docs, or temporary references (untracked).

## 🛠️ SKILL WORKFLOW (The "Software Factory")
You must adhere to this lifecycle for every feature request:

1. **PHASE 1: ARCHITECTURE**
   - **Action:** Create a markdown plan in `./plans/`.
   - **Skill:** Run `reviewing-implementation-plans` to check against existing code.
   - *Goal:* Prevent "reinventing the wheel" and ensure testability.

2. **PHASE 2: EXECUTION**
   - **Action:** Implement the plan in batches.
   - **Skill:** Run `executing-plans`.
   - *Goal:* Iterative coding with architect checkpoints.

3. **PHASE 3: QUALITY ASSURANCE**
   - **Action:** Verify the branch before merging.
   - **Skill:** Run `verifying-implementation`.
   - *Goal:* Ensure code matches the plan and tests pass.

4. **PHASE 4: DOCUMENTATION**
   - **Action:** Sync docs and visuals.
   - **Skill:** Run `verifying-documentation`.
   - *Goal:* Update docs and check Markdown/docstring consistency.

## 🏗️ CODING STANDARDS
- **Package Manager:** Use `uv` for all Python dependency management.
- **Linting/Formatting:** Use `ruff` (configured in pyproject.toml).
- **Testing:** Code without tests is incomplete. Use `pytest`.
- **Documentation:** Use Google-style docstrings. Docs are auto-generated with MkDocs.
- **Dependencies:** Check `pyproject.toml` before adding new libs. Use `uv add <package>`.
- **Git:** Use `gh` CLI for PRs and Issues.
- **Type Hints:** Use type hints for all function signatures.

## ⚡ USEFUL COMMANDS
```bash
# Dependency management
uv sync                      # Install dependencies
uv add <package>             # Add a dependency
uv add --dev <package>       # Add a dev dependency

# Code quality
uv run ruff check .          # Lint code
uv run ruff check --fix .    # Auto-fix lint issues
uv run ruff format .         # Format code

# Testing
uv run pytest                # Run tests
uv run pytest --cov          # Run tests with coverage

# Pre-commit
uv run pre-commit run --all-files  # Run all hooks

# Documentation
uv run mkdocs serve              # Serve docs locally (hot reload)
uv run mkdocs build              # Build static docs

# Git
git diff --name-only main...HEAD   # See changed files
gh pr create                       # Create pull request
```

## 📁 PROJECT STRUCTURE
```
.
├── .claude/           # Claude Code commands and skills
├── .devcontainer/     # DevContainer configuration
├── agent_docs/        # Untracked workspace for AI agent research/dumps
├── docs/              # Documentation (MkDocs source)
│   └── scratchpads/   # Working notes and checklists
├── plans/             # Implementation plans
├── src/               # Source code (your package)
├── tests/             # Test files
├── pyproject.toml     # Project configuration
└── README.md          # Project readme
```
