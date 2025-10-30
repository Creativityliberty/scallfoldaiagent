# 🚀 Quickstart - Agent IA Gemini MCP

Guide de démarrage ultra-rapide pour lancer l'agent IA en 5 minutes !

## ⚡ Installation Express

```bash
# 1. Cloner et entrer dans le projet
cd agent-ia-gemini-mcp

# 2. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate

# 3. Installer les dépendances
pip install -e .
```

## 🔑 Configuration

```bash
# Créer le fichier .env
cat > .env << 'EOF'
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash-latest
HOST=0.0.0.0
PORT=8000
DEBUG=true
VECTOR_STORE_DIM=768
MAX_CONTEXT_LENGTH=8000
MCP_SERVER_NAME=agent-ia-mcp
MCP_VERSION=1.0.0
EOF

# IMPORTANT: Éditer .env et remplacer your_gemini_api_key_here
# Obtenir une clé gratuite ici: https://ai.google.dev/
```

## ▶️ Lancer l'application

```bash
# Méthode 1: Uvicorn direct
uvicorn backend.main:app --reload --port 8000

# Méthode 2: Python module
python -m backend.main

# Méthode 3: Avec hot reload
uvicorn backend.main:app --reload --log-level info
```

Ouvrir → **http://localhost:8000** 🎉

## 🧪 Tester l'API

```bash
# Health check
curl http://localhost:8000/health

# MCP tools
curl http://localhost:8000/api/mcp/tools

# Chat (exemple)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"input": "Bonjour, explique-moi RRLA"}'
```

## 📦 Avec Docker (optionnel)

```bash
# Build
docker build -t agent-ia .

# Run
docker run -p 8000:8000 --env-file .env agent-ia
```

## 🐛 Dépannage

### Erreur "GEMINI_API_KEY not found"
→ Vérifier que le fichier `.env` existe et contient la clé

### Erreur "Module not found"
→ Vérifier que l'environnement virtuel est activé et les dépendances installées

### Port 8000 déjà utilisé
→ Changer le port : `uvicorn backend.main:app --port 8001`

## 🎓 Premiers pas

1. **Chat simple**
   - Ouvrir http://localhost:8000
   - Taper "Bonjour"
   - Voir la réponse de l'agent

2. **Mode streaming**
   - Cocher "Mode streaming (SSE)"
   - Observer les tokens arriver en temps réel

3. **Debug trace**
   - Cocher "Afficher la trace"
   - Voir le détail de l'exécution (nodes, durée, confiance)

4. **Tester MCP**
   ```bash
   curl -X POST http://localhost:8000/api/mcp/call \
     -H "Content-Type: application/json" \
     -d '{"tool": "calculate", "arguments": {"expression": "2 + 2"}}'
   ```

## 📚 Documentation complète

Voir [README.md](README.md) pour la documentation complète

## 💬 Besoin d'aide ?

Ouvrir une issue : https://github.com/votre-repo/issues

---

**Happy coding! 🚀**
