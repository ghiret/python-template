# Python Template

A Python project template optimized for development with Claude Code and uv.

## Features

- **uv** for fast Python dependency management
- **Claude Code** as the primary coding agent
- **DevContainer** for consistent development environment
- **Ruff** for linting and formatting (auto-applied via hooks)
- **pre-commit** hooks for code quality
- **pytest** + **hypothesis** for testing
- **Custom skills & agents** for structured workflows
- **Plugin** for cross-repo reuse

## Quick Start

### Using DevContainer (Recommended)

1. Clone this repository
2. Open in VS Code
3. When prompted, click "Reopen in Container"
4. Claude Code will be automatically installed on container start

### Local Development

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync --all-extras

# Install pre-commit hooks
uv run pre-commit install

# Install Claude Code
curl -fsSL https://claude.ai/install.sh | bash
```

### Git Authentication in DevContainer

The DevContainer doesn't have SSH keys by default. To push:

```bash
# Option 1: Use GitHub CLI (recommended)
gh auth login
git push origin main

# Option 2: Switch to HTTPS
git remote set-url origin https://github.com/<user>/<repo>.git
git push origin main
```

## Project Structure

```
.
├── .claude/              # Claude Code configuration
│   ├── skills/           # Workflow skills (/execute, /verify, etc.)
│   ├── agents/           # Subagents (code-reviewer, test-writer, security-reviewer)
│   ├── hooks/            # Auto-format, file protection, compaction context
│   ├── rules/            # Path-specific coding rules
│   ├── commands/         # Command wrappers
│   └── settings.json     # Permissions and hook config
├── python-factory-plugin/ # Installable plugin for other repos
├── .devcontainer/        # DevContainer configuration
├── src/                  # Source code
├── tests/                # Test files
├── plans/                # Implementation plans
├── pyproject.toml        # Project configuration
└── README.md
```

## Development

### Running Tests

```bash
uv run pytest
uv run pytest --cov --cov-report=html  # With coverage
uv run pytest -m "not slow"            # Skip slow tests
```

### Linting & Formatting

Ruff auto-formats Python files after every edit via a PostToolUse hook. To run manually:

```bash
uv run ruff check .
uv run ruff check --fix .
uv run ruff format .
```

### Using Claude Code

```bash
# Start Claude Code
claude
```

### Skill Workflow (The "Software Factory")

Every feature follows this lifecycle:

1. **Plan** — Write a plan in `plans/`, run `/review-plan plans/my-feature.md`
2. **Execute** — Implement in batches with `/execute plans/my-feature.md`
3. **Verify** — QA check with `/verify`
4. **Document** — Sync docs with `/verify-docs`

### Autonomous Workflow (Ralph)

For fully autonomous development with built-in review loops and per-phase commits:

```bash
# Auto-review until approved (up to 5 iterations)
/ralph-review plans/my-feature.md

# Auto-execute with verification and commits per phase
/ralph-execute plans/my-feature.md

# Custom iteration counts
/ralph-review 3 plans/my-feature.md
/ralph-execute 10 plans/my-feature.md
```

### Available Subagents

| Agent | Model | Purpose |
|-------|-------|---------|
| code-reviewer | Sonnet | Code quality, security, ruff compliance |
| test-writer | Inherit | Generate pytest + hypothesis tests |
| security-reviewer | Opus | Focused security vulnerability audit |

## Using as a Plugin

The skills, agents, and hooks can be installed as a plugin in other repos:

```bash
# One-liner: clone and use
claude --plugin-dir /path/to/python-template/python-factory-plugin

# Skills are namespaced when used as a plugin:
# /python-factory:execute, /python-factory:review-plan, etc.
```

## License

MIT
