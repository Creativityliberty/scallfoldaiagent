# 🧠 Agent IA Complet - Gemini + MCP + PocketFlow

Agent IA de production avec architecture modulaire inspirée de **PocketFlow**, **RRLA** et le protocole **MCP** (Model Context Protocol).

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🏗️ Architecture

```
┌─────────────┐
│   Frontend  │  HTML/CSS/JS → Interface utilisateur moderne
└──────┬──────┘
       │
┌──────▼──────┐
│   FastAPI   │  REST + SSE → Endpoints API
└──────┬──────┘
       │
┌──────▼──────────────────────┐
│   Orchestrator (PocketFlow) │  → Coordonne le flow
└──────┬──────────────────────┘
       │
       ├─→ Perception       → Nettoie l'input
       ├─→ Interpretation   → Détecte l'intention
       ├─→ Memory          → Recherche contexte
       ├─→ Reasoning (RRLA)→ Raisonnement en 4 étapes
       ├─→ Synthesis       → Génère la réponse
       └─→ Action          → Retourne le résultat

┌──────────────┐
│ Gemini LLM   │  → Génération + Streaming
└──────────────┘

┌──────────────┐
│ MCP Server   │  → Outils extensibles
└──────────────┘
```

## 🎯 Fonctionnalités

### ✅ Core
- 🧠 **Architecture RRLA** : Raisonnement → Réflexion → Logique → Action
- 🔄 **PocketFlow** : Pattern prep/exec/post avec shared contract
- 🔌 **MCP Protocol** : Outils extensibles via Model Context Protocol
- 🚀 **Streaming SSE** : Génération token-par-token en temps réel
- 📊 **Traçabilité complète** : Debug trace de chaque exécution

### 🛠️ Nodes Implémentés
1. **Perception** : Nettoyage et normalisation des entrées
2. **Interprétation** : Détection d'intention et typage de tâche
3. **Memory** : Recherche contexte conversationnel
4. **Reasoning** : RRLA complet avec décomposition en étapes
5. **Synthesis** : Agrégation et génération de réponse
6. **Action** : Production de la réponse finale

### 🔧 Outils MCP
- `search_memory` : Recherche sémantique dans la mémoire
- `store_memory` : Stockage d'éléments en mémoire
- `analyze_sentiment` : Analyse de sentiment
- `extract_keywords` : Extraction de mots-clés
- `calculate` : Évaluateur d'expressions mathématiques
- `get_current_context` : Récupération du contexte agent

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11+
- Clé API Gemini ([obtenir ici](https://ai.google.dev/))

### Installation

```bash
# 1. Cloner le repo
git clone <votre-repo>
cd agent-ia-gemini-mcp

# 2. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -e .

# Ou avec uv (plus rapide)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
uv sync
```

### Configuration

```bash
# Copier le template .env
cp .env.example .env

# Éditer .env et ajouter votre clé Gemini
# GEMINI_API_KEY=your_key_here
```

### Lancer l'application

```bash
# Avec uvicorn directement
uvicorn backend.main:app --reload --port 8000

# Ou via Python
python -m backend.main

# Ou avec uv
uv run uvicorn backend.main:app --reload --port 8000
```

Ouvrir **http://localhost:8000** dans votre navigateur 🎉

## 📚 Documentation API

### Endpoints REST

```bash
# Chat classique (non-streaming)
POST /api/chat
{
  "input": "Explique-moi l'architecture RRLA",
  "user_id": "user123"
}

# Streaming SSE
GET /api/stream?prompt=Bonjour

# Informations MCP
GET /api/mcp/info
GET /api/mcp/tools
GET /api/mcp/tools/schema

# Appel d'outil MCP
POST /api/mcp/call
{
  "tool": "search_memory",
  "arguments": {"query": "test", "top_k": 5}
}

# Pipeline info
GET /api/pipeline/info

# Health check
GET /health

# Statistiques
GET /api/stats
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=backend --cov-report=html

# Test spécifique
pytest tests/test_orchestrator.py -v
```

## 🎨 Frontend

L'interface web inclut :
- **Chat conversationnel** avec historique
- **Mode streaming** via Server-Sent Events
- **Panneau debug** avec trace d'exécution
- **Indicateurs de confiance** pour chaque réponse
- **Design moderne** dark theme

### Raccourcis clavier
- `Ctrl+K` : Effacer la conversation
- `Ctrl+D` : Toggle panneau debug
- `Ctrl+S` : Toggle mode streaming
- `Shift+Enter` : Toggle streaming (dans l'input)

## 🏗️ Structure du Projet

```
agent-ia-gemini-mcp/
├─ backend/
│  ├─ core/                # PocketFlow core
│  │  ├─ shared.py         # Contract de données
│  │  ├─ base_node.py      # Interface Node
│  │  └─ orchestrator.py   # Orchestrateur central
│  ├─ nodes/               # Modules fonctionnels
│  │  ├─ perception.py
│  │  ├─ interpretation.py
│  │  ├─ reasoning.py      # RRLA
│  │  ├─ synthesis.py
│  │  ├─ action.py
│  │  └─ memory.py
│  ├─ llm/                 # Client Gemini
│  │  ├─ gemini_client.py
│  │  ├─ prompt_builder.py
│  │  └─ token_counter.py
│  ├─ mcp/                 # MCP Server
│  │  ├─ server.py
│  │  ├─ tools.py
│  │  └─ schemas.py
│  ├─ memory/              # Système mémoire
│  │  ├─ vector_store.py
│  │  ├─ graph_memory.py
│  │  └─ context_manager.py
│  ├─ utils/               # Utilitaires
│  │  ├─ logger.py
│  │  └─ validators.py
│  ├─ main.py              # FastAPI app
│  └─ config.py            # Configuration
├─ frontend/               # Interface web
│  ├─ index.html
│  ├─ styles.css
│  └─ app.js
├─ tests/                  # Tests unitaires
├─ pyproject.toml          # Dépendances
└─ README.md
```

## 🔧 Configuration Avancée

### Variables d'environnement

```bash
# API
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-1.5-flash-latest  # ou gemini-1.5-pro

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Memory
VECTOR_STORE_DIM=768
MAX_CONTEXT_LENGTH=8000

# MCP
MCP_SERVER_NAME=agent-ia-mcp
MCP_VERSION=1.0.0
```

## 🎓 Architecture RRLA

Le système de raisonnement RRLA se décompose en 4 étapes :

### 1. Raisonnement (R1)
Décompose le problème en étapes logiques
```
"Créer un site web" → [
  1. Choisir la stack technique
  2. Créer la structure HTML
  3. Styliser avec CSS
  4. Ajouter l'interactivité JS
]
```

### 2. Réflexion (R2)
Évalue chaque étape (faisabilité, priorité, risques)
```
Étape 1: feasibility=0.9, priority=5, risks=[]
Étape 2: feasibility=0.8, priority=4, risks=["complexité"]
```

### 3. Logique (L)
Construit la chaîne d'exécution
```
sequence: [1, 2, 3, 4]
critical_path: [1, 2]
dependencies: {3: [2], 4: [2, 3]}
```

### 4. Action (A)
Décide et exécute
```
action_type: "generate_response"
confidence: 0.85
requires_tools: false
```

## 🔌 Étendre avec MCP

### Ajouter un nouvel outil

```python
# 1. Créer la fonction handler
async def mon_outil(param1: str, param2: int) -> dict:
    # Logique de l'outil
    return {"result": "ok"}

# 2. Définir le schéma
MON_OUTIL_SCHEMA = {
    "type": "object",
    "properties": {
        "param1": {"type": "string"},
        "param2": {"type": "integer"}
    },
    "required": ["param1"]
}

# 3. Enregistrer l'outil
from backend.mcp import mcp_server, MCPTool

mcp_server.register_tool(MCPTool(
    name="mon_outil",
    description="Description de l'outil",
    input_schema=MON_OUTIL_SCHEMA,
    handler=mon_outil
))
```

## 📊 Performance

| Opération | Temps moyen |
|-----------|-------------|
| Perception | ~5ms |
| Interprétation | ~10ms |
| Raisonnement (simple) | ~50ms |
| Raisonnement (RRLA) | ~500ms |
| Synthèse | ~800ms |
| **Total (simple)** | **~100ms** |
| **Total (RRLA)** | **~1.4s** |

*Tests sur machine moyenne avec Gemini 1.5 Flash*

## 🐛 Debugging

### Activer les logs détaillés

```python
from backend.utils.logger import setup_logger
setup_logger(log_level="DEBUG", log_file="logs/agent.log")
```

### Inspecter le flow

```python
# Via l'API
result = await orchestrator.run(shared)
trace = shared.get_trace()

for entry in trace:
    print(f"{entry.node}: {entry.status} ({entry.duration_ms}ms)")
```

## 🤝 Contribution

Les contributions sont bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/ma-feature`)
3. Commit (`git commit -m 'Ajoute ma feature'`)
4. Push (`git push origin feature/ma-feature`)
5. Ouvrir une Pull Request

### Style de code
- Black pour le formatage
- Ruff pour le linting
- Type hints partout
- Docstrings pour les fonctions publiques

## 📝 Roadmap

- [ ] Intégration vector store (FAISS)
- [ ] Système de mémoire long terme
- [ ] Support multi-modèles (OpenAI, Anthropic)
- [ ] Authentification utilisateurs
- [ ] Mode multi-agents
- [ ] Plugins dynamiques
- [ ] Interface de configuration web
- [ ] Métriques et analytics

## 📄 Licence

MIT License - voir [LICENSE](LICENSE)

## 🙏 Remerciements

- [Google Gemini](https://ai.google.dev/) pour le LLM
- [FastAPI](https://fastapi.tiangolo.com/) pour le framework web
- [PocketFlow](https://github.com/hamada-ai/pocket-flow) pour l'inspiration architecture
- [MCP](https://www.anthropic.com/news/model-context-protocol) pour le protocole d'outils

## 📧 Contact

Pour toute question : [ouvrir une issue](https://github.com/votre-repo/issues)

---

**Fait avec ❤️ et ☕ par [Votre Nom]**
