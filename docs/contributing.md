# Contributing

Thank you for your interest in contributing!

## Development Setup

1. Fork and clone the repository
2. Install dependencies:
   ```bash
   uv sync --all-extras
   ```
3. Install pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```

## Code Style

This project uses:

- **Ruff** for linting and formatting
- **Google-style docstrings**
- **Type hints** for all function signatures

### Running Checks

```bash
# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check (if mypy is added)
uv run mypy src/
```

## Testing

All new features should include tests:

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov --cov-report=html
```

## Documentation

Update documentation for any new features:

```bash
# Serve docs locally
uv run mkdocs serve
```

Add docstrings to all public functions and classes.

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a pull request

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `chore:` Maintenance tasks
- `refactor:` Code refactoring
- `test:` Test additions or changes
