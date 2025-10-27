#!/bin/bash
# Quick start script for Agent IA + GitMCP

echo "🚀 Agent IA + GitMCP - Quick Start"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "✅ In project directory"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv (Python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "✅ uv available"

# Create virtual environment
echo "📦 Setting up virtual environment..."
uv venv

# Install dependencies
echo "📥 Installing dependencies..."
source .venv/bin/activate
uv sync

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. cp .env.example .env"
echo "2. Edit .env and add: GEMINI_API_KEY=your_api_key_here"
echo "3. uv run uvicorn backend.main:app --reload --port 8000"
echo ""
echo "🌐 Then visit: http://localhost:8000"
echo ""
echo "🎯 Features ready to test:"
echo "• Paste GitHub URLs (github.com/user/repo)"
echo "• Click '📦 Charger Repo' to load context"
echo "• Ask questions about the codebase"
echo "• Toggle streaming mode"
echo "• View debug traces"
echo ""
echo "Happy coding! 🎉"
