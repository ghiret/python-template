# Installation

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager

## Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Clone and Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_PROJECT.git
cd YOUR_PROJECT

# Install dependencies
uv sync --all-extras

# Install pre-commit hooks
uv run pre-commit install
```

## Using DevContainer (Recommended)

If you're using VS Code with the DevContainers extension:

1. Open the project in VS Code
2. Click "Reopen in Container" when prompted
3. Claude Code will be automatically installed on container start

## Verify Installation

```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Build docs locally
uv run mkdocs serve
```
