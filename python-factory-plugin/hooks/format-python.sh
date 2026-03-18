#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only format Python files
if [[ "$FILE_PATH" != *.py ]]; then
  exit 0
fi

# Run ruff check + format; never block Claude on formatter errors
uv run ruff check --fix --quiet "$FILE_PATH" 2>/dev/null
uv run ruff format --quiet "$FILE_PATH" 2>/dev/null
exit 0
