# ⚡ Quick Start - Agent IA + GitMCP

Démarrage rapide en 3 minutes.

## 1️⃣ Installation (1 min)

```bash
cd agent-ia-gemini-mcp

# Créer l'environnement
uv venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows

# Installer les dépendances principales (sans torch)
uv sync

# OPTIONNEL: Installer les dépendances mémoire (si vous voulez FAISS/torch)
uv sync --extra memory
```

## 2️⃣ Configuration (1 min)

```bash
# Copier le fichier d'env
cp .env.example .env

# Éditer .env et ajouter votre clé Gemini
# GEMINI_API_KEY=AIzaSyD6vHyVe8gyr3SSZXlrN2l68UZWr_GmVqI
```

## 3️⃣ Lancer (1 min)

```bash
uv run uvicorn backend.main:app --reload --port 8000
```

Ouvrir [http://localhost:8000](http://localhost:8000) 🎉

## 🎯 Utilisation

### Charger un repo GitHub

1. Colle une URL GitHub dans le champ "📦 Charger Repo"
   ```
   github.com/username/repo
   ```

2. Clique sur le bouton ou appuie sur Entrée

3. Attends le statut ✅

### Poser une question

1. Écris ta question dans le champ de chat

2. Clique "Envoyer" ou appuie sur Entrée

3. Le contexte repo est automatiquement injecté

### Mode Streaming

Coche "Mode streaming (SSE)" pour voir les réponses token par token.

### Voir la trace

Coche "Afficher la trace" pour voir les timings de chaque node.

## 📋 Commandes utiles

```bash
# Tests
uv run pytest tests/ -v

# Linter
uv run ruff check backend/

# Type checking
uv run mypy backend/

# Voir les logs
DEBUG=true uv run uvicorn backend.main:app --reload
```

## 🔗 Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Interface web |
| `/api/chat` | POST | Chat REST |
| `/api/stream` | GET | Chat SSE (streaming) |
| `/api/gitmcp/fetch` | POST | Charger repo GitHub |
| `/api/mcp/tools` | GET | Lister outils MCP |
| `/api/mcp/call` | POST | Appeler outil MCP |
| `/health` | GET | Health check |

## 📚 Documentation

- [README.md](./README.md) - Architecture complète
- [GITMCP_INTEGRATION.md](./GITMCP_INTEGRATION.md) - Détails GitMCP
- [backend/](./backend/) - Code source

## 🐛 Troubleshooting

**Erreur: "GEMINI_API_KEY not found"**
→ Vérifier que `.env` contient votre clé API

**Erreur: "Port 8000 already in use"**
→ Utiliser un autre port: `--port 8001`

**Erreur: "Module not found"**
→ Relancer `uv sync`

**Erreur: "torch not available"**
→ Les fonctionnalités mémoire utilisent des fallbacks simples

**GitMCP: "Repo not found"**
→ Vérifier que l'URL est correcte et le repo public

## 🚀 Prochaines étapes

1. Charger un repo GitHub
2. Poser une question sur le code
3. Voir l'agent analyser le contexte
4. Ajouter des outils MCP personnalisés
5. Intégrer avec d'autres services

Bon coding! 🎉

Bon coding! 🎉
