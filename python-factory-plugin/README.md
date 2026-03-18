# Python Factory Plugin

A Claude Code plugin providing a complete Python project workflow: plan, review, execute, verify, document.

## Installation

### Local development (from this repo)

```bash
claude --plugin-dir /path/to/python-template/python-factory-plugin
```

### From another project

```bash
git clone https://github.com/ghiret/python-template /tmp/python-factory
claude --plugin-dir /tmp/python-factory/python-factory-plugin
```

## Skills

All skills are namespaced as `/python-factory:<skill-name>` when installed as a plugin.

| Skill | Command | Description |
|-------|---------|-------------|
| execute | `/python-factory:execute` | Execute implementation plans in batches with review checkpoints |
| review-plan | `/python-factory:review-plan` | Architect review: redundancy, architecture, testability checks |
| fix-plan | `/python-factory:fix-plan` | Surgical fixes to plans based on review feedback |
| verify | `/python-factory:verify` | Post-execution QA: plan compliance, redundancy audit, tests |
| verify-docs | `/python-factory:verify-docs` | Sync documentation with code, generate architecture diagrams |
| init-project | `/python-factory:init-project` | Initialize a new project from the template |
| web-design-guidelines | `/python-factory:web-design-guidelines` | Review UI code for Web Interface Guidelines compliance |

## Agents

| Agent | Model | Description |
|-------|-------|-------------|
| code-reviewer | Sonnet | Read-only code review for quality, security, ruff compliance |
| test-writer | Inherit | Generate pytest + hypothesis tests, run and verify |
| security-reviewer | Opus | Focused security audit with severity ratings |

## Hooks

| Hook | Event | Description |
|------|-------|-------------|
| format-python.sh | PostToolUse (Edit/Write) | Auto-format Python files with ruff |
| protect-files.sh | PreToolUse (Edit/Write) | Block edits to uv.lock, .env, .github/workflows/ |
| post-compact-context.sh | SessionStart (compact) | Re-inject dynamic context after compaction |

## Requirements

- `jq` must be installed for hook scripts to parse JSON input
- `uv` and `ruff` for the format hook
- `git` for the compact context hook

## License

MIT
