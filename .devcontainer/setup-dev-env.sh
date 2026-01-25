#!/bin/bash
# Setup development environment for Claude Code

set -e

echo "🔧 Setting up development environment..."

# Install Claude Code (always get latest version)
echo "📦 Installing Claude Code..."
curl -fsSL https://claude.ai/install.sh | bash

# Add Claude to PATH for current session if not already there
if [[ ":$PATH:" != *":$HOME/.claude/bin:"* ]]; then
    export PATH="$HOME/.claude/bin:$PATH"
fi

# Verify installation
if command -v claude &> /dev/null; then
    echo "✅ Claude Code installed successfully: $(claude --version 2>/dev/null || echo 'version check not available')"
else
    echo "⚠️  Claude Code installation completed but 'claude' command not found in PATH"
    echo "   Try restarting your terminal or run: export PATH=\"\$HOME/.claude/bin:\$PATH\""
fi

echo "🎉 Development environment setup complete!"
