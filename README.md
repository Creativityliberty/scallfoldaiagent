# 🧠 Agent IA Complet - Gemini + MCP + PocketFlow

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Agent IA de production avec architecture modulaire inspirée de PocketFlow, RRLA et le protocole MCP. Intégration GitMCP pour charger automatiquement le contexte des repos GitHub.

## ✨ Fonctionnalités

- **🧠 Architecture PocketFlow**: Nodes modulaires avec contrat Shared (contexte, résultats, trace)
- **🔄 Raisonnement RRLA**: Raisonnement, Réflexion, Logique, Action
- **🔗 Protocole MCP**: Outils exposés via function calling
- **📦 GitMCP Integration**: Charge automatiquement le contexte des repos GitHub
- **⚡ Streaming SSE**: Réponses token-par-token en temps réel
- **🎨 Interface Moderne**: UI dark avec chat, trace, et contrôles
- **🛡️ Production-Ready**: Logging, retry, error handling, tests

## 🚀 Démarrage Rapide

```bash
# 1. Cloner le repo
git clone https://github.com/Creativityliberty/scallfoldaiagent.git
cd scallfoldaiagent

# 2. Installer les dépendances
./install.sh

# 3. Configurer la clé API
cp .env.example .env
# Éditer .env: GEMINI_API_KEY=votre_clé_ici

# 4. Lancer le serveur
uv run uvicorn backend.main:app --reload --port 8000
```

Ouvrir [http://localhost:8000](http://localhost:8000) 🎉

## 🎯 Utilisation

### 1. Charger un Repo GitHub
```bash
# Colle une URL dans l'interface
github.com/username/repo
# → Clique "📦 Charger Repo"
# → ✅ Contexte chargé automatiquement
```

### 2. Poser des Questions
```bash
"Explique l'architecture de ce projet"
"Quels sont les fichiers principaux?"
"Comment fonctionne le système RRLA?"
```

### 3. Fonctionnalités Avancées
- **Mode Streaming**: Cochez pour voir les réponses en temps réel
- **Trace Debug**: Affichez les timings de chaque node
- **Outils MCP**: Le serveur expose des outils via `/api/mcp/`

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Browser)                       │
├─────────────────────────────────────────────────────────────────┤
│  GitMCP Input → Chat Interface → Streaming Display → Debug Trace  │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                           │
├─────────────────────────────────────────────────────────────────┤
│  POST /api/gitmcp/fetch → MCP Tools → PocketFlow Orchestrator   │
│  ↓                        ↓            ↓                          │
│  GitMCPClient           MCPServer    RRLA Nodes                  │
│  ↓                        ↓            ↓                          │
│  Fetch llms.txt        Tool Calling  Perception → Reasoning     │
│  README.md             Function Call  ↓           ↓              │
└──────────────────────────────────────┼───────────┼──────────────┘
                                       ↓           ↓
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL APIs                               │
├─────────────────────────────────────────────────────────────────┤
│  gitmcp.io (Context) → Gemini API (LLM) → GitHub (Optional)     │
└─────────────────────────────────────────────────────────────────┘
```

### Nodes PocketFlow

1. **Perception**: Nettoyage et normalisation des entrées
2. **Interprétation**: Détection d'intention et typage
3. **Raisonnement (RRLA)**: Décomposition → Réflexion → Logique → Action
4. **Synthèse**: Agrégation des résultats
5. **Action**: Production de la réponse finale

## 📦 Structure du Projet

```
scallfoldaiagent/
├─ 📄 README.md                 # Documentation
├─ 📄 QUICKSTART.md            # Guide rapide
├─ 📄 GITMCP_INTEGRATION.md    # Détails GitMCP
├─ 📄 ARCHITECTURE_GITMCP.md   # Diagrammes
├─ 📄 CHANGES.md               # Historique
├─ 🚀 install.sh               # Script d'installation
├─ ⚙️ pyproject.toml           # Dépendances
├─ 🔧 .env.example             # Variables d'environnement
├─ 🚫 .gitignore               # Fichiers ignorés
│
├─ 🖥️ backend/                 # API FastAPI
│  ├─ main.py                  # Point d'entrée
│  ├─ config.py                # Configuration Pydantic
│  ├─ core/                    # Architecture PocketFlow
│  │  ├─ shared.py             # Contrat Shared
│  │  ├─ base_node.py          # Interface Node
│  │  └─ orchestrator.py       # Coordinateur
│  ├─ nodes/                   # Implémentations RRLA
│  │  ├─ perception.py
│  │  ├─ interpretation.py
│  │  ├─ reasoning.py
│  │  ├─ synthesis.py
│  │  ├─ action.py
│  │  └─ feedback.py
│  ├─ llm/                     # Client Gemini
│  │  ├─ gemini_client.py
│  │  ├─ prompt_builder.py
│  │  └─ token_counter.py
│  ├─ mcp/                     # Protocole MCP
│  │  ├─ server.py
│  │  ├─ tools.py
│  │  └─ schemas.py
│  ├─ integrations/            # Intégrations externes
│  │  └─ gitmcp.py             # Client GitMCP
│  ├─ memory/                  # Stockage (optionnel)
│  │  ├─ vector_store.py
│  │  ├─ graph_memory.py
│  │  └─ context_manager.py
│  └─ utils/                   # Utilitaires
│     ├─ logger.py
│     └─ validators.py
│
├─ 🌐 frontend/                # Interface web
│  ├─ index.html               # Page principale
│  ├─ app.js                   # Logique JavaScript
│  └─ styles.css               # Styles modernes
│
└─ 🧪 tests/                   # Tests unitaires
   ├─ test_orchestrator.py
   ├─ test_nodes.py
   └─ test_mcp.py
```

## 🔗 Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Interface web |
| `/api/chat` | POST | Chat REST |
| `/api/stream` | GET | Chat SSE (streaming) |
| `/api/gitmcp/fetch` | POST | Charger repo GitHub |
| `/api/mcp/tools` | GET | Lister outils MCP |
| `/api/mcp/call` | POST | Appeler outil MCP |
| `/health` | GET | Health check |

## 🧪 Tests

```bash
# Lancer tous les tests
uv run pytest tests/ -v

# Avec coverage
uv run pytest tests/ --cov=backend

# Tests MCP uniquement
uv run pytest tests/test_mcp.py -v
```

## 📚 Documentation

- **[QUICKSTART.md](./QUICKSTART.md)** - Guide de démarrage (3 min)
- **[GITMCP_INTEGRATION.md](./GITMCP_INTEGRATION.md)** - Intégration GitMCP
- **[ARCHITECTURE_GITMCP.md](./ARCHITECTURE_GITMCP.md)** - Diagrammes système
- **[CHANGES.md](./CHANGES.md)** - Historique des modifications

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Distribué sous licence MIT. Voir `LICENSE` pour plus d'informations.

## 🙏 Remerciements

- **PocketFlow** pour l'architecture modulaire
- **GitMCP** pour l'intégration de contexte GitHub
- **Google Gemini** pour le modèle de langage
- **FastAPI** pour le framework web

## 📞 Contact

Créé par [Creativityliberty](https://github.com/Creativityliberty)

---

**⭐ Star ce repo si vous trouvez ça utile!**
# Agent IA Complet - Gemini + MCP + PocketFlow + GitMCP
