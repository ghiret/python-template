# Quick Start

## Initialize Your Project

After cloning the template, run the `initialize-project` command in Claude Code:

```
/project:initialize-project
```

This will prompt you to configure:

- Project name
- Description
- Author information
- License
- GitHub repository

## Project Structure

```
.
├── .claude/           # Claude Code commands and skills
├── .devcontainer/     # DevContainer configuration
├── docs/              # Documentation (MkDocs)
├── plans/             # Implementation plans
├── src/               # Source code
├── tests/             # Test files
├── pyproject.toml     # Project configuration
└── mkdocs.yml         # Documentation configuration
```

## Development Workflow

### 1. Create a Plan

Before implementing a feature, create a plan in `plans/`:

```markdown
# Feature: My New Feature

## Overview
Brief description of the feature.

## Implementation Steps
1. Step one
2. Step two
3. Step three

## Testing
- Test case 1
- Test case 2
```

### 2. Review the Plan

```
/project:review-plan plans/my-feature.md
```

### 3. Execute the Plan

```
/project:execute-plan plans/my-feature.md
```

### 4. Verify Implementation

```
/project:verify-implementation plans/my-feature.md
```

## Adding Dependencies

```bash
# Add a runtime dependency
uv add requests

# Add a dev dependency
uv add --dev httpx
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_example.py
```

## Building Documentation

```bash
# Serve docs locally (with hot reload)
uv run mkdocs serve

# Build static docs
uv run mkdocs build
```
