#!/bin/bash
set -euo pipefail

# Python Factory Installer
# Install Claude Code skills, agents, hooks, and rules from python-template
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/ghiret/python-template/main/install.sh | bash
#
#   # Or with options:
#   curl -fsSL https://raw.githubusercontent.com/ghiret/python-template/main/install.sh | bash -s -- --plugin
#   curl -fsSL https://raw.githubusercontent.com/ghiret/python-template/main/install.sh | bash -s -- --branch feature/claude2-comp

REPO="ghiret/python-template"
BRANCH="main"
MODE="direct"  # direct = copy into .claude/, plugin = copy plugin dir
TMPDIR=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --plugin)
      MODE="plugin"
      shift
      ;;
    --branch)
      BRANCH="$2"
      shift 2
      ;;
    --help)
      echo "Python Factory Installer"
      echo ""
      echo "Installs Claude Code skills, agents, hooks, and rules from ghiret/python-template."
      echo ""
      echo "Usage:"
      echo "  curl -fsSL https://raw.githubusercontent.com/ghiret/python-template/main/install.sh | bash"
      echo ""
      echo "Options:"
      echo "  --plugin     Install as a plugin directory instead of copying into .claude/"
      echo "  --branch X   Use a specific branch (default: main)"
      echo "  --help       Show this help"
      echo ""
      echo "Modes:"
      echo "  direct (default)  Copies skills, agents, hooks, rules, settings into .claude/"
      echo "  --plugin          Clones python-factory-plugin/ for use with claude --plugin-dir"
      exit 0
      ;;
    *)
      echo "Unknown option: $1. Use --help for usage."
      exit 1
      ;;
  esac
done

cleanup() {
  if [ -n "$TMPDIR" ] && [ -d "$TMPDIR" ]; then
    rm -rf "$TMPDIR"
  fi
}
trap cleanup EXIT

echo "Python Factory Installer"
echo "========================"
echo "Repo:   $REPO"
echo "Branch: $BRANCH"
echo "Mode:   $MODE"
echo ""

# Check prerequisites
if ! command -v git &> /dev/null; then
  echo "Error: git is required but not installed."
  exit 1
fi

# Clone to temp directory (shallow, single branch)
TMPDIR=$(mktemp -d)
echo "Cloning $REPO@$BRANCH..."
git clone --depth 1 --branch "$BRANCH" "https://github.com/$REPO.git" "$TMPDIR/repo" --quiet

SRC="$TMPDIR/repo"

if [ "$MODE" = "plugin" ]; then
  # Plugin mode: copy the plugin directory
  if [ ! -d "$SRC/python-factory-plugin" ]; then
    echo "Error: python-factory-plugin/ not found in repo."
    exit 1
  fi

  TARGET="python-factory-plugin"
  if [ -d "$TARGET" ]; then
    echo "Removing existing $TARGET/..."
    rm -rf "$TARGET"
  fi

  cp -r "$SRC/python-factory-plugin" "$TARGET"
  echo ""
  echo "Installed plugin to ./$TARGET/"
  echo ""
  echo "Usage:"
  echo "  claude --plugin-dir ./python-factory-plugin"
  echo ""
  echo "Skills are namespaced: /python-factory:execute, /python-factory:review-plan, etc."

else
  # Direct mode: copy into .claude/
  echo ""

  # Remove old skill directories (pre-rename names)
  OLD_SKILLS=(
    executing-plans
    fixing-implementation-plans
    initializing-projects
    reviewing-implementation-plans
    verifying-implementation
    verifying-documentation
  )
  for old in "${OLD_SKILLS[@]}"; do
    if [ -d ".claude/skills/$old" ]; then
      echo "Removing old skill: $old/"
      rm -rf ".claude/skills/$old"
    fi
  done

  # Create directories
  mkdir -p .claude/skills .claude/agents .claude/hooks .claude/rules .claude/commands

  # Copy skills
  echo "Installing skills..."
  for skill_dir in "$SRC/.claude/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    rm -rf ".claude/skills/$skill_name"
    cp -r "$skill_dir" ".claude/skills/$skill_name"
    echo "  $skill_name"
  done

  # Copy agents
  echo "Installing agents..."
  for agent_file in "$SRC/.claude/agents"/*.md; do
    agent_name=$(basename "$agent_file")
    cp "$agent_file" ".claude/agents/$agent_name"
    echo "  $agent_name"
  done

  # Copy hooks
  echo "Installing hooks..."
  for hook_file in "$SRC/.claude/hooks"/*; do
    hook_name=$(basename "$hook_file")
    cp "$hook_file" ".claude/hooks/$hook_name"
    chmod +x ".claude/hooks/$hook_name" 2>/dev/null || true
    echo "  $hook_name"
  done

  # Copy rules
  echo "Installing rules..."
  for rule_file in "$SRC/.claude/rules"/*.md; do
    rule_name=$(basename "$rule_file")
    cp "$rule_file" ".claude/rules/$rule_name"
    echo "  $rule_name"
  done

  # Copy commands
  echo "Installing commands..."
  for cmd_file in "$SRC/.claude/commands"/*.md; do
    cmd_name=$(basename "$cmd_file")
    cp "$cmd_file" ".claude/commands/$cmd_name"
    echo "  $cmd_name"
  done

  # Copy settings.json (merge or overwrite)
  if [ -f ".claude/settings.json" ]; then
    echo ""
    echo "WARNING: .claude/settings.json already exists."
    echo "  New settings saved to: .claude/settings.json.new"
    echo "  Please merge manually to preserve your existing permissions/hooks."
    cp "$SRC/.claude/settings.json" ".claude/settings.json.new"
  else
    cp "$SRC/.claude/settings.json" ".claude/settings.json"
    echo "Installing settings.json"
  fi

  # Verify
  echo ""
  echo "Verification:"
  SKILL_COUNT=$(ls -d .claude/skills/*/ 2>/dev/null | wc -l)
  AGENT_COUNT=$(ls .claude/agents/*.md 2>/dev/null | wc -l)
  HOOK_COUNT=$(ls .claude/hooks/*.sh 2>/dev/null | wc -l)
  RULE_COUNT=$(ls .claude/rules/*.md 2>/dev/null | wc -l)
  echo "  Skills: $SKILL_COUNT"
  echo "  Agents: $AGENT_COUNT"
  echo "  Hooks:  $HOOK_COUNT"
  echo "  Rules:  $RULE_COUNT"

  # Check for jq
  if ! command -v jq &> /dev/null; then
    echo ""
    echo "WARNING: jq is not installed. Hook scripts require jq to parse JSON input."
    echo "  Install with: sudo apt-get install jq (Debian/Ubuntu) or brew install jq (macOS)"
  fi

  echo ""
  echo "Installation complete!"
  echo ""
  echo "Available skills:"
  echo "  /review-plan    - Architect review of implementation plans"
  echo "  /fix-plan       - Fix plans based on review feedback"
  echo "  /execute        - Execute plans in batches"
  echo "  /verify         - Post-execution QA"
  echo "  /review-docs    - Detect documentation drift"
  echo "  /fix-docs       - Update text documentation from drift findings"
  echo "  /generate-diagrams - Generate or update architecture diagrams"
  echo "  /generate-images   - Generate AI documentation images"
  echo "  /init-project   - Initialize from template"
  echo "  /ralph-review   - Autonomous review loop (N iterations)"
  echo "  /ralph-execute  - Autonomous execute + verify + commit pipeline"
fi

echo ""
echo "Done."
