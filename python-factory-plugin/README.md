# Python Factory Plugin

A Claude Code plugin providing a complete Python project workflow: plan, review, execute, verify, document.

HTML is the preferred artifact format for implementation plans and generated reports. Markdown plans remain supported. Shared conventions live in `skills/_shared/html-conventions.md` and `skills/_shared/testing-conventions.md`.

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
| execute | `/python-factory:execute` | Execute HTML or Markdown implementation plans in batches |
| review-plan | `/python-factory:review-plan` | Architect review: redundancy, architecture, testability, phase structure, and test budget checks |
| fix-plan | `/python-factory:fix-plan` | Surgical fixes to plans based on review feedback |
| verify | `/python-factory:verify` | Post-execution QA: plan compliance, redundancy audit, tests |
| review-docs | `/python-factory:review-docs` | Detect documentation drift in text, diagrams, and images |
| fix-docs | `/python-factory:fix-docs` | Update text documentation from a drift report |
| generate-diagrams | `/python-factory:generate-diagrams` | Generate or update architecture diagrams |
| generate-images | `/python-factory:generate-images` | Generate AI documentation images |
| init-project | `/python-factory:init-project` | Initialize a new project from the template |
| ralph-review | `/python-factory:ralph-review` | Autonomous review loop for implementation plans |
| ralph-execute | `/python-factory:ralph-execute` | Autonomous full-plan or selected-phase execution pipeline |
| web-design-guidelines | `/python-factory:web-design-guidelines` | Review UI code for Web Interface Guidelines compliance |

## Artifact Conventions

- Plans: `agent_docs/plans/*.html` preferred, `*.md` supported
- Review reports: `agent_docs/reports/reviews/*.html`
- Verification reports: `agent_docs/reports/verify/*.html`
- Documentation drift reports: `agent_docs/reports/drift/*.html`
- Unit tests should be fast; no unit test should exceed 60 seconds unless reclassified as a marked long-running integration/e2e/load test.

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
