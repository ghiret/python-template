# Python Template

A Python project template optimized for development with Claude Code and uv.

## Features

- **uv** for fast Python dependency management
- **Claude Code** as the primary coding agent
- **DevContainer** for consistent development environment
- **Ruff** for linting and formatting
- **pre-commit** hooks for code quality
- **pytest** for testing

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

## Project Structure

```
.
├── .claude/           # Claude Code configuration and skills
├── .devcontainer/     # DevContainer configuration
├── src/               # Source code
├── tests/             # Test files
├── pyproject.toml     # Project configuration
└── README.md
```

## Development

### Running Tests

```bash
uv run pytest
```

### Linting & Formatting

```bash
# Run ruff linter
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Using Claude Code

```bash
# Start Claude Code
claude
```

## License

MIT
