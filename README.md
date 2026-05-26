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
├── .agents/              # Codex-compatible skills
├── AGENTS.md             # Codex project guidance
├── python-factory-plugin/ # Installable plugin for other repos
├── .devcontainer/        # DevContainer configuration
├── src/                  # Source code
├── tests/                # Test files
├── agent_docs/plans/     # HTML/Markdown implementation plans (ignored)
├── agent_docs/reports/   # Agent-generated review/verify/drift reports (ignored)
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

### Skill Layout

The repo supports both runtimes:

- `.claude/skills/` uses Claude-compatible frontmatter, including `disable-model-invocation` for manually triggered workflow skills.
- `.agents/skills/` keeps Codex-compatible copies of the same skill bodies; tests verify they stay synchronized with `.claude/skills/`.
- `python-factory-plugin/skills/` carries the Claude-compatible plugin copy.

### Skill Workflow (The "Software Factory")

Every feature follows this lifecycle:

1. **Plan** — Write an HTML plan in `agent_docs/plans/`, run `/review-plan agent_docs/plans/my-feature.html`. Markdown plans still work.
2. **Execute** — Implement in batches with `/execute agent_docs/plans/my-feature.html`
3. **Verify Tests** — Fast test-quality audit with `/verify-tests`
4. **Verify** — QA check with `/verify`
5. **Document** — Audit with `/review-docs`, then run `/fix-docs`, `/generate-diagrams`, or `/generate-images` as needed

Plans and reports follow `.claude/skills/_shared/html-conventions.md`. Tests follow `.claude/skills/_shared/testing-conventions.md`: unit tests should be fast, no unit test may exceed 60 seconds, and long integration/e2e tests must be marked separately.

Use `/html-artifact` for self-contained browser-readable artifacts that are not executable plans or standard reports, such as exploration grids, PR explainers, design prototypes, and throwaway editors.

### Autonomous Workflow (Ralph)

For fully autonomous development with built-in review loops and per-phase commits:

```bash
# Auto-review until approved (up to 5 iterations)
/ralph-review agent_docs/plans/my-feature.html

# Auto-execute with test-quality gates, verification, and commits per phase
/ralph-execute agent_docs/plans/my-feature.html

# Custom drift review iteration count
/ralph-review 3 agent_docs/plans/my-feature.html
/ralph-execute 10 agent_docs/plans/my-feature.html

# Execute selected phases only
/ralph-execute phase=2 agent_docs/plans/my-feature.html
/ralph-execute phases=2-4 agent_docs/plans/my-feature.html
/ralph-execute 3 phases=1,3 agent_docs/plans/my-feature.html
```

### Available Subagents

| Agent | Model | Purpose |
|-------|-------|---------|
| code-reviewer | Sonnet | Code quality, security, ruff compliance |
| test-writer | Inherit | Generate pytest + hypothesis tests |
| security-reviewer | Opus | Focused security vulnerability audit |

## Installing in Other Projects

### One-liner install (copies into .claude/)

```bash
curl -fsSL https://raw.githubusercontent.com/ghiret/python-template/main/install.sh | bash
```

This installs the Claude-compatible skills, Codex-compatible skill copies, 3 agents, 3 hooks, 3 rules, and command wrappers into your project.

**What it does:**
- Detects and removes old-named skills (`executing-plans`, `verifying-implementation`, etc.)
- Copies new skills by name — your custom skills are untouched
- Copies Codex-compatible skills into `.agents/skills/`
- Preserves `settings.local.json` and any personal files in `.claude/`
- If `settings.json` already exists, saves the new one as `settings.json.new` for manual merge
- Warns if `jq` is missing (required for hooks)

**What it does NOT do:**
- Delete your custom skills, commands, or agents
- Overwrite `settings.local.json`
- Touch files outside `.claude/` and `.agents/`

### Install as a plugin (no changes to your repo)

```bash
curl -fsSL https://raw.githubusercontent.com/ghiret/python-template/main/install.sh | bash -s -- --plugin
```

This copies `python-factory-plugin/` into your project. Use with:

```bash
claude --plugin-dir ./python-factory-plugin
```

Skills are namespaced: `/python-factory:execute`, `/python-factory:ralph-review`, etc.

### Options

```bash
# Use a specific branch
curl -fsSL https://raw.githubusercontent.com/ghiret/python-template/main/install.sh | bash -s -- --branch feature/my-branch

# Show help
curl -fsSL https://raw.githubusercontent.com/ghiret/python-template/main/install.sh | bash -s -- --help
```

## License

MIT
