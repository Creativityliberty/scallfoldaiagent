#!/bin/bash
# Installation script for Agent IA + GitMCP

echo "🚀 Installation Agent IA + GitMCP"
echo "=================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv n'est pas installé. Installez-le avec:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ uv trouvé"

# Create venv
echo "📦 Création de l'environnement virtuel..."
uv venv

# Activate venv
echo "🔄 Activation de l'environnement..."
source .venv/bin/activate

# Install dependencies (without torch)
echo "📥 Installation des dépendances..."
uv sync

echo ""
echo "✅ Installation terminée!"
echo ""
echo "📋 Prochaines étapes:"
echo "1. cp .env.example .env"
echo "2. Éditez .env avec votre clé Gemini: GEMINI_API_KEY=..."
echo "3. uv run uvicorn backend.main:app --reload --port 8000"
echo ""
echo "🎉 Ouvrez http://localhost:8000"
echo ""
echo "💡 Note: Les fonctionnalités mémoire utilisent des fallbacks simples"
echo "    pour éviter les problèmes de compatibilité torch."
