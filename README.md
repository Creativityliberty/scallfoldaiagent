# 🧠 Agent IA Complet - Gemini + MCP + PocketFlow

Agent IA de production avec architecture modulaire inspirée de PocketFlow, RRLA et le protocole MCP.

## 🏗️ Architecture

- Backend: FastAPI + Python 3.11+
- LLM: Google Gemini (streaming + function calling)
- Orchestration: PocketFlow (Nodes + Shared contract)
- Protocole: MCP (Model Context Protocol)
- Frontend: HTML/JS/CSS vanilla (pas de Node requis)

```
agent-ia-gemini-mcp/
├─ pyproject.toml
├─ .env.example
├─ README.md
├─ backend/
│  ├─ main.py
│  ├─ config.py
│  ├─ core/
│  │  ├─ shared.py
│  │  ├─ orchestrator.py
│  │  └─ base_node.py
│  ├─ nodes/
│  │  ├─ perception.py
│  │  ├─ interpretation.py
│  │  ├─ reasoning.py
│  │  ├─ synthesis.py
│  │  ├─ action.py
│  │  └─ feedback.py
│  ├─ llm/
│  │  ├─ gemini_client.py
│  │  ├─ prompt_builder.py
│  │  └─ token_counter.py
│  ├─ mcp/
│  │  ├─ server.py
│  │  ├─ tools.py
│  │  └─ schemas.py
│  ├─ memory/
│  │  ├─ vector_store.py
│  │  ├─ graph_memory.py
│  │  └─ context_manager.py
│  └─ utils/
│     ├─ logger.py
│     └─ validators.py
├─ frontend/
│  ├─ index.html
│  ├─ app.js
│  └─ styles.css
└─ tests/
   ├─ test_orchestrator.py
   ├─ test_nodes.py
   └─ test_mcp.py
```

## 🚀 Démarrage Rapide

1) Installation

```bash
# Installer uv (gestionnaire Python ultra-rapide)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Aller dans le dossier
cd agent-ia-gemini-mcp

# Créer l'environnement virtuel
uv venv

# Installer les dépendances
uv sync
```

2) Configuration

```bash
# Copier le template .env
cp .env.example .env
# Ouvrir .env et définir votre clé
# GEMINI_API_KEY=your_key_here
```

3) Lancer

```bash
# Activer l'environnement
source .venv/bin/activate        # Linux/Mac
# .venv\\Scripts\\activate       # Windows

# Démarrer l'API (auto-reload)
uv run uvicorn backend.main:app --reload --port 8000
```

Ouvrir http://localhost:8000

## 📋 Fonctionnalités

- Perception: Nettoyage et normalisation des entrées
- Interprétation: Détection d'intention et typage de tâche
- Raisonnement (RRLA): Décomposition, réflexion, logique, action
- Synthèse: Agrégation des résultats
- Action: Production de la réponse finale
- SSE Streaming: Token-par-token en temps réel
- MCP Server: Outils exposés via protocole
- Traçabilité: Trace complète de chaque exécution

## 🎯 Endpoints API

- GET  /                    – Interface web
- POST /api/chat            – Chat REST (non-streaming)
- GET  /api/stream          – Chat SSE (streaming)
- GET  /api/mcp/info        – Info serveur MCP
- GET  /api/mcp/tools       – Liste des outils MCP
- POST /api/mcp/call        – Appel d'un outil MCP
- GET  /health              – Health check

## 🧪 Tests

```bash
uv run pytest tests/ -v --cov=backend
```

Les tests mockent l'API Gemini pour éviter tout appel réseau.

## 📚 Notes d'Architecture

- RRLA
  - R – Raisonnement: Décomposition du problème
  - R – Réflexion: Évaluation des options
  - L – Logique: Chaînage d'inférences
  - A – Action: Prise de décision
- MCP
  - Outils exposés via `backend/mcp/server.py`
  - Exemple: `search_memory`

### Shared Contract (PocketFlow)

Toutes les données transitent par le `Shared` store:

```python
shared.set_context("user_input", text)
shared.set_result("reasoning", decision)
shared.add_trace(entry)
```

## 🛠️ Développement

Ajouter un Node

```python
# backend/nodes/mon_node.py
from backend.core.base_node import BaseNode

class MonNode(BaseNode):
    def __init__(self):
        super().__init__("mon_node")
    async def exec(self, input_data):
        return {"result": "..."}
```

Enregistrer dans l'orchestrateur si nécessaire.

Ajouter un Outil MCP

```python
from backend.mcp.server import mcp_server, MCPTool

async def mon_outil(param: str) -> dict:
    return {"resultat": f"Traité: {param}"}

mcp_server.register_tool(MCPTool(
    name="mon_outil",
    description="Description de l'outil",
    input_schema={
        "type": "object",
        "properties": {"param": {"type": "string"}}
    },
    handler=mon_outil
))
```

## ✅ Production-Ready

- Retry logic et streaming pour Gemini
- Orchestrateur modulaire
- Lazy-init du client LLM (tests sans env vars)
- Logging structuré
- Tests unitaires avec mocks

## 📄 Licence

MIT
