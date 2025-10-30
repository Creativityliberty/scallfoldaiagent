# 🧠 Agent Framework v2.0.0 - Gemini + MCP + PocketFlow

Agent IA de production avec architecture modulaire et agents spécialisés, inspirée de **PocketFlow**, **RRLA** et le protocole **MCP** (Model Context Protocol).

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Version](https://img.shields.io/badge/version-2.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🆕 Nouveautés v2.0.0

- 🤖 **3 Agents Spécialisés** : Lead Generator, Social Media Manager, WordPress Blogger
- 🛠️ **20+ Outils MCP** : Outils organisés par domaine (web scraping, social media, WordPress, content)
- 📚 **Exemples Complets** : 4 scripts démontrant toutes les capacités
- ⚙️ **Configuration YAML** : Système de configuration flexible et extensible
- 🚀 **Scripts de Déploiement** : Support multi-plateformes (Docker, systemd, cloud)
- 📊 **Nouveaux Endpoints API** : Gestion et exécution d'agents via REST API

## 🏗️ Architecture v2.0.0

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Interfaces                  │
│  • Chat UI  • Agent Dashboard  • WordPress Dashboard   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    FastAPI Server                        │
│  REST API + SSE + WebSocket + Static Files              │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
┌────────▼─────┐ ┌──────▼──────┐ ┌─────▼──────────────┐
│ Orchestrator │ │   Agents    │ │   MCP Server       │
│ (PocketFlow) │ │   System    │ │   & Tools          │
└──────────────┘ └─────────────┘ └────────────────────┘
│                │               │
│ • Perception   │ • Lead Gen    │ • Web Scraping     │
│ • Interpret    │ • Social Med  │ • Social Media     │
│ • Memory       │ • WordPress   │ • WordPress        │
│ • Reasoning    │               │ • Content Gen      │
│ • Synthesis    │               │ • Memory & More    │
│ • Action       │               │                    │
└────────────────┴───────────────┴────────────────────┘
                         │
                ┌────────▼─────────┐
                │   Gemini LLM     │
                │  (Flash/Pro)     │
                └──────────────────┘
```

## 🎯 Fonctionnalités

### ✅ Core (v1.0)
- 🧠 **Architecture RRLA** : Raisonnement → Réflexion → Logique → Action
- 🔄 **PocketFlow** : Pattern prep/exec/post avec shared contract
- 🔌 **MCP Protocol** : Outils extensibles via Model Context Protocol
- 🚀 **Streaming SSE** : Génération token-par-token en temps réel
- 📊 **Traçabilité complète** : Debug trace de chaque exécution

### 🤖 Agents Disponibles (v2.0)

#### 1️⃣ Lead Generator Agent
Génération et qualification de leads B2B
- 🔍 Recherche sur Google Maps
- 📧 Extraction d'emails professionnels
- 📊 Enrichissement de données
- ✅ Qualification automatique
- 📦 Traitement par batch

**Exemple d'utilisation:**
```python
from backend.agents import LeadGeneratorAgent

agent = LeadGeneratorAgent()
result = await agent.execute({
    "query": "tech startups",
    "location": "San Francisco, CA",
    "max_results": 50
})
# Returns: {"status": "success", "leads": [...], "count": 50}
```

#### 2️⃣ Social Media Manager Agent
Création et gestion de contenu social media
- 📱 Génération de posts multi-plateformes
- 📅 Création de calendriers éditoriaux
- #️⃣ Recherche de hashtags pertinents
- 🖼️ Génération de prompts d'images
- 📊 Analyse de performance

**Exemple d'utilisation:**
```python
from backend.agents import SocialMediaManagerAgent

agent = SocialMediaManagerAgent()
campaign = await agent.create_campaign(
    topic="Product Launch",
    duration_days=7,
    platforms=["twitter", "linkedin", "instagram"]
)
# Returns: {"status": "success", "total_posts": 21, ...}
```

#### 3️⃣ WordPress Blogger Agent
Création d'articles SEO optimisés pour WordPress
- ✍️ Génération d'articles complets
- 🔎 Recherche de mots-clés SEO
- 📈 Calcul de score SEO (Yoast compatible)
- 🖼️ Génération d'images mises en avant
- 🚀 Publication automatique sur WordPress

**Exemple d'utilisation:**
```python
from backend.agents import WordPressBloggerAgent

agent = WordPressBloggerAgent(
    wordpress_url="https://monsite.com",
    target_word_count=1800
)
result = await agent.execute({
    "topic": "Guide complet du Machine Learning",
    "publish": True
})
# Returns: {"status": "success", "seo_score": 85, "post_url": "..."}
```

### 🛠️ MCP Tools (20+ outils)

#### Web Scraping & Lead Generation
- `search_google_maps` - Recherche de businesses
- `extract_business_email` - Extraction d'emails
- `enrich_lead_data` - Enrichissement de données
- `qualify_lead` - Qualification de leads
- `save_leads_to_db` - Sauvegarde en base

#### Social Media
- `generate_social_post` - Génération de posts
- `create_content_calendar` - Calendrier éditorial
- `hashtag_research` - Recherche de hashtags
- `generate_image_prompt` - Prompts d'images DALL-E
- `analyze_post_performance` - Analyse de performance

#### WordPress & Blogging
- `research_keywords` - Recherche mots-clés SEO
- `generate_article_content` - Génération d'articles
- `calculate_seo_score` - Score SEO Yoast
- `create_wordpress_post` - Publication WordPress
- `generate_featured_image` - Image mise en avant
- `fetch_stock_images` - Images Unsplash
- `optimize_image` - Optimisation d'images
- `set_yoast_seo_meta` - Métadonnées Yoast

#### Content Generation
- `generate_text` - Génération de texte
- `summarize_content` - Résumés
- `improve_content` - Amélioration
- `generate_outline` - Plans d'articles
- `generate_headlines` - Titres accrocheurs
- `check_plagiarism` - Vérification originalité

### 🛠️ Nodes du Pipeline (RRLA)
1. **Perception** : Nettoyage et normalisation
2. **Interprétation** : Détection d'intention
3. **Memory** : Recherche contexte
4. **Reasoning** : RRLA (4 étapes)
5. **Synthesis** : Génération réponse
6. **Action** : Production résultat

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11+
- Clé API Gemini ([obtenir ici](https://ai.google.dev/))
- (Optionnel) Clés API : Google Places, DALL-E, Unsplash
- (Optionnel) Site WordPress pour l'agent blogger

### Installation Automatique (Recommandé)

```bash
# 1. Cloner le repo
git clone https://github.com/Creativityliberty/scallfoldaiagent.git
cd scallfoldaiagent

# 2. Lancer le script d'installation
chmod +x scripts/run_agent.sh
./scripts/run_agent.sh
```

Le script va:
- ✅ Créer l'environnement virtuel
- ✅ Installer les dépendances
- ✅ Créer les fichiers de configuration
- ✅ Proposer un menu interactif pour démarrer

### Installation Manuelle

```bash
# 1. Cloner le repo
git clone https://github.com/Creativityliberty/scallfoldaiagent.git
cd scallfoldaiagent

# 2. Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install --upgrade pip
pip install fastapi uvicorn[standard] google-genai pydantic pydantic-settings \
    python-dotenv httpx loguru beautifulsoup4 pillow

# 4. Configuration
cp .env.example .env
# Éditer .env avec vos clés API
```

### Configuration

#### Configuration Minimale (Requise)
```bash
# Copier le template
cp .env.example .env

# Éditer .env et ajouter votre clé Gemini (OBLIGATOIRE)
GEMINI_API_KEY=votre_cle_gemini_ici
```

#### Configuration Complète (Optionnelle)
```bash
# APIs Externes (pour fonctionnalités avancées)
GOOGLE_PLACES_API_KEY=votre_cle      # Lead Generator
DALLE_API_KEY=votre_cle              # Génération d'images
UNSPLASH_API_KEY=votre_cle           # Images stock

# WordPress (pour WordPress Blogger Agent)
WORDPRESS_URL=https://monsite.com
WORDPRESS_ENABLED=true

# Configuration SEO
TARGET_WORD_COUNT=1800
MIN_SEO_SCORE=70
```

#### Configuration WordPress (Optionnelle)
Si vous voulez utiliser le WordPress Blogger Agent:

```bash
# Méthode 1: Script automatique
./scripts/setup_wordpress.sh

# Méthode 2: Manuel
# 1. Générer un Application Password dans WordPress:
#    Users → Your Profile → Application Passwords
# 2. Ajouter dans .env:
WORDPRESS_URL=https://monsite.com
WORDPRESS_USERNAME=votre_username
WORDPRESS_PASSWORD=votre_application_password
```

### Lancer l'application

```bash
# Méthode 1: Script interactif (Recommandé)
./scripts/run_agent.sh

# Méthode 2: Uvicorn directement
uvicorn backend.main:app --reload --port 8000

# Méthode 3: Python module
python -m backend.main
```

**Accès aux interfaces:**
- 💬 **Chat Principal**: http://localhost:8000
- 🤖 **Dashboard Agents**: http://localhost:8000/dashboard
- ✍️ **WordPress UI**: http://localhost:8000/wordpress
- 📖 **API Docs**: http://localhost:8000/docs

## 📚 Documentation API

### Endpoints Core (v1.0)

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

### Endpoints Agents (v2.0) 🆕

```bash
# Lister tous les agents
GET /api/agents
# Response: {"agents": [...], "count": 3}

# Exécuter Lead Generator
POST /api/agents/lead_generator/execute
{
  "query": "restaurants",
  "location": "Paris, France",
  "max_results": 50
}

# Exécuter Social Media Manager
POST /api/agents/social_media/execute
{
  "type": "post",
  "topic": "AI Innovation",
  "platform": "linkedin",
  "tone": "professional"
}

# Exécuter WordPress Blogger
POST /api/agents/wordpress/execute
{
  "topic": "Machine Learning Guide",
  "word_count": 1800,
  "publish": false
}

# Dashboard HTML
GET /dashboard

# WordPress UI HTML  
GET /wordpress
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

## 📁 Exemples d'Utilisation

### Exemple 1: Lead Generation Complète

```python
import asyncio
from backend.agents import LeadGeneratorAgent

async def main():
    agent = LeadGeneratorAgent()
    
    # Recherche simple
    leads = await agent.search_businesses(
        query="tech startups",
        location="San Francisco, CA",
        max_results=50
    )
    
    # Traitement par batch
    result = await agent.batch_process(
        queries=["SaaS", "AI companies", "Tech consulting"],
        location="New York, NY"
    )
    
    print(f"Total leads: {result['total_leads']}")

asyncio.run(main())
```

### Exemple 2: Campagne Social Media

```python
import asyncio
from backend.agents import SocialMediaManagerAgent

async def main():
    agent = SocialMediaManagerAgent()
    
    # Créer une campagne complète
    campaign = await agent.create_campaign(
        topic="Product Launch 2025",
        duration_days=7,
        platforms=["twitter", "linkedin", "instagram"]
    )
    
    print(f"Posts créés: {campaign['total_posts']}")
    
    # Recherche de hashtags
    result = await agent.execute({
        "type": "hashtags",
        "topic": "AI Technology",
        "platform": "twitter"
    })

asyncio.run(main())
```

### Exemple 3: Article WordPress SEO

```python
import asyncio
from backend.agents import WordPressBloggerAgent

async def main():
    agent = WordPressBloggerAgent(
        wordpress_url="https://monsite.com"
    )
    
    # Génération d'article
    result = await agent.execute({
        "topic": "Guide Complet Python 2025",
        "word_count": 2000,
        "tone": "educational",
        "publish": True
    })
    
    print(f"SEO Score: {result['seo_score']['overall']}/100")
    print(f"Article URL: {result.get('post_url')}")
    
    # Génération batch
    articles = await agent.batch_generate([
        "Python Best Practices",
        "Web Development Trends",
        "Cloud Computing Guide"
    ])

asyncio.run(main())
```

### Exemple 4: Workflow Complet

```python
import asyncio
from backend.agents import (
    LeadGeneratorAgent,
    SocialMediaManagerAgent,
    WordPressBloggerAgent
)

async def marketing_workflow():
    # 1. Générer des leads
    lead_agent = LeadGeneratorAgent()
    leads = await lead_agent.execute({
        "query": "AI startups",
        "location": "San Francisco"
    })
    
    # 2. Créer campagne social media
    social_agent = SocialMediaManagerAgent()
    campaign = await social_agent.create_campaign(
        topic="Best AI Startups SF",
        duration_days=5
    )
    
    # 3. Écrire article de blog
    blog_agent = WordPressBloggerAgent()
    article = await blog_agent.execute({
        "topic": "Top AI Startups in San Francisco 2025"
    })
    
    return {
        "leads_count": leads["count"],
        "posts_created": campaign["total_posts"],
        "article_seo": article["seo_score"]["overall"]
    }

asyncio.run(marketing_workflow())
```

**Fichiers d'exemples complets disponibles:**
- `examples/lead_generator_agent.py` - 6 exemples Lead Generator
- `examples/social_media_manager_agent.py` - 6 exemples Social Media
- `examples/wordpress_blog_agent.py` - 6 exemples WordPress
- `examples/complete_agent_example.py` - Workflows intégrés

```bash
# Exécuter les exemples
python examples/lead_generator_agent.py
python examples/social_media_manager_agent.py
python examples/wordpress_blog_agent.py
python examples/complete_agent_example.py
```

## 🏗️ Structure du Projet v2.0

```
scallfoldaiagent/
├─ backend/
│  ├─ agents/                    # 🆕 Agents spécialisés
│  │  ├─ __init__.py
│  │  ├─ base_agent.py           # Classe de base
│  │  ├─ lead_generator.py       # Lead generation
│  │  ├─ social_media_manager.py # Social media
│  │  └─ wordpress_blogger.py    # WordPress blogging
│  ├─ mcp/
│  │  ├─ server.py               # MCP Server
│  │  ├─ tools.py                # Outils de base
│  │  ├─ schemas.py
│  │  └─ tool_modules/           # 🆕 Outils spécialisés
│  │     ├─ web_scraping.py      # Lead generation tools
│  │     ├─ social_media.py      # Social media tools
│  │     ├─ wordpress.py         # WordPress tools
│  │     └─ content.py           # Content generation
│  ├─ core/                      # PocketFlow core
│  │  ├─ shared.py
│  │  ├─ base_node.py
│  │  └─ orchestrator.py
│  ├─ nodes/                     # RRLA Pipeline
│  │  ├─ perception.py
│  │  ├─ interpretation.py
│  │  ├─ reasoning.py
│  │  ├─ synthesis.py
│  │  ├─ action.py
│  │  └─ memory.py
│  ├─ llm/                       # LLM Client
│  │  ├─ gemini_client.py
│  │  └─ ...
│  ├─ memory/                    # Memory System
│  ├─ utils/                     # Utilities
│  ├─ main.py                    # FastAPI app
│  └─ config.py                  # Configuration
├─ frontend/                     # Interfaces web
│  ├─ index.html                 # Chat UI
│  ├─ agent-dashboard.html       # 🆕 Agent Dashboard
│  ├─ wordpress-dashboard.html   # 🆕 WordPress UI
│  ├─ styles.css
│  └─ app.js
├─ examples/                     # 🆕 Exemples complets
│  ├─ lead_generator_agent.py
│  ├─ social_media_manager_agent.py
│  ├─ wordpress_blog_agent.py
│  └─ complete_agent_example.py
├─ config/                       # 🆕 Configuration YAML
│  ├─ agent_config.yaml
│  ├─ wordpress_config.yaml
│  └─ mcp_tools_config.yaml
├─ scripts/                      # 🆕 Scripts utilitaires
│  ├─ run_agent.sh               # Quick start
│  ├─ setup_wordpress.sh         # WordPress setup
│  └─ deploy.sh                  # Déploiement
├─ docs/                         # 🆕 Documentation
├─ tests/                        # Tests unitaires
├─ .env.example                  # Template configuration
├─ pyproject.toml                # Dépendances
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

## 🚀 Déploiement

### Déploiement Local (Development)
```bash
./scripts/deploy.sh
# Choisir option 1
```

### Déploiement Docker
```bash
./scripts/deploy.sh
# Choisir option 2
# Puis: docker-compose up -d
```

### Déploiement Production (systemd)
```bash
./scripts/deploy.sh
# Choisir option 3
# Puis suivre les instructions affichées
```

### Déploiement Cloud (Heroku/Railway/Render)
```bash
./scripts/deploy.sh
# Choisir option 4
# Fichiers générés: Procfile, runtime.txt, render.yaml
```

## 📊 Performance & Benchmarks

### Agents (v2.0)
| Agent | Opération | Temps moyen | Débit |
|-------|-----------|-------------|-------|
| Lead Generator | Single search (10 leads) | ~150ms | 66 leads/s |
| Lead Generator | Batch (50 leads) | ~500ms | 100 leads/s |
| Social Media | Single post | ~100ms | 10 posts/s |
| Social Media | Campaign (21 posts) | ~800ms | 26 posts/s |
| WordPress | Article (1800 mots) | ~2.5s | 720 mots/s |
| WordPress | Batch (3 articles) | ~6s | 900 mots/s |

### Pipeline RRLA (v1.0)
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

## 📝 Roadmap

### v2.1.0 (À venir)
- [ ] Interfaces frontend complètes (Dashboard & WordPress UI)
- [ ] WebSocket pour updates en temps réel
- [ ] Support API keys externes (Google Places, DALL-E, Unsplash)
- [ ] Tests E2E pour tous les agents
- [ ] Documentation API interactive (Swagger UI étendu)

### v2.2.0
- [ ] Agent Email Marketing (4ème agent)
- [ ] Agent CRM Integration (5ème agent)
- [ ] Intégration vector store (FAISS) pour agents
- [ ] Système de mémoire long terme partagée
- [ ] Plugins dynamiques pour agents

### v3.0.0 (Future)
- [ ] Support multi-modèles (OpenAI, Anthropic, Local LLMs)
- [ ] Authentification et multi-tenancy
- [ ] Mode multi-agents avec orchestration
- [ ] Interface de configuration web complète
- [ ] Métriques et analytics temps réel
- [ ] API GraphQL en plus de REST

## 🧪 Tests

### Exécuter les tests
```bash
# Tests unitaires (quand disponibles)
pytest tests/ -v

# Tests avec couverture
pytest tests/ --cov=backend --cov-report=html

# Tester les agents manuellement
python examples/lead_generator_agent.py
python examples/social_media_manager_agent.py
python examples/wordpress_blog_agent.py
```

### Tests API via curl
```bash
# Test health
curl http://localhost:8000/health

# Test agents list
curl http://localhost:8000/api/agents

# Test lead generator
curl -X POST http://localhost:8000/api/agents/lead_generator/execute \
  -H "Content-Type: application/json" \
  -d '{"query":"restaurants","location":"Paris","max_results":10}'
```

## 📄 Licence

MIT License - voir [LICENSE](LICENSE)

## 🙏 Remerciements

- [Google Gemini](https://ai.google.dev/) pour le LLM
- [FastAPI](https://fastapi.tiangolo.com/) pour le framework web
- [PocketFlow](https://github.com/hamada-ai/pocket-flow) pour l'inspiration architecture
- [MCP](https://www.anthropic.com/news/model-context-protocol) pour le protocole d'outils

## 💼 Cas d'Usage

### Marketing Digital
- 🎯 Génération de leads qualifiés
- 📱 Gestion de campagnes social media
- ✍️ Content marketing automatisé

### Agences
- 👥 Lead generation pour clients
- 📊 Rapports et analytics automatiques
- 🔄 Workflows multi-clients

### Startups & PME
- 💰 Réduction des coûts marketing
- ⚡ Accélération de la production de contenu
- 📈 Scalabilité sans équipe large

## 📧 Support & Contact

- 🐛 **Bugs**: [Ouvrir une issue](https://github.com/Creativityliberty/scallfoldaiagent/issues)
- 💡 **Suggestions**: [Discussions GitHub](https://github.com/Creativityliberty/scallfoldaiagent/discussions)
- 📖 **Documentation**: Voir `/docs` (en développement)
- 📧 **Email**: Créer une issue pour questions

## 🌟 Contribuer

Les contributions sont les bienvenues! Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.

### Quick Start pour Contributeurs
```bash
# 1. Fork & Clone
git clone https://github.com/YOUR_USERNAME/scallfoldaiagent.git

# 2. Créer une branche
git checkout -b feature/amazing-feature

# 3. Développer & Tester
# ... vos modifications ...

# 4. Commit & Push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# 5. Ouvrir une Pull Request
```

---

**Agent Framework v2.0.0** - Fait avec ❤️ par [@Creativityliberty](https://github.com/Creativityliberty)
