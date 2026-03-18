#!/bin/bash
echo "Post-compaction context refresh:"

# Show recently modified files (lost during compaction)
MODIFIED=$(git diff --name-only HEAD 2>/dev/null | head -20)
if [ -n "$MODIFIED" ]; then
  echo "Files modified in working tree:"
  echo "$MODIFIED" | sed 's/^/  - /'
fi

# Detect active implementation plan
ACTIVE_PLAN=$(ls -t plans/*.md 2>/dev/null | head -1)
if [ -n "$ACTIVE_PLAN" ]; then
  echo "Most recent plan: $ACTIVE_PLAN"
fi

echo "Coding standards are in CLAUDE.md. Path-specific rules are in .claude/rules/."
exit 0
