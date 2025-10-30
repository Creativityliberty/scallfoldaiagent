# 🎨 Guide Complet - Artifacts Skill MCP

## 📋 Vue d'ensemble

Le système d'**Artifacts** permet à l'agent IA de créer, gérer et sauvegarder des fichiers (code, documents, configurations, données) via le protocole MCP.

## 🏗️ Architecture

```
Agent IA
    ↓
MCP Server
    ↓
Artifact Tools (5 outils)
    ↓
Artifact Store (stockage en mémoire)
    ↓
Fichiers sur disque (optionnel)
```

## 🔧 Outils MCP Disponibles

### 1. `create_artifact` - Créer un artifact

Crée un nouvel artifact (code, document, config, data).

**Paramètres:**
```json
{
  "name": "script.py",          // Nom du fichier
  "type": "code",               // code|document|data|config
  "content": "print('Hello')",  // Contenu
  "language": "python",         // Optionnel (auto-détecté)
  "description": "Script test", // Optionnel
  "metadata": {}                // Optionnel
}
```

**Réponse:**
```json
{
  "success": true,
  "artifact": {
    "id": "artifact_12345",
    "name": "script.py",
    "type": "code",
    "language": "python",
    "content": "print('Hello')",
    "size_bytes": 14,
    "lines": 1,
    "created_at": "2025-10-28T12:00:00Z"
  }
}
```

### 2. `save_artifact` - Sauvegarder sur disque

Sauvegarde un artifact vers un fichier.

**Paramètres:**
```json
{
  "artifact_id": "artifact_12345",
  "path": "/path/to/script.py",
  "create_dirs": true
}
```

**Réponse:**
```json
{
  "success": true,
  "path": "/absolute/path/to/script.py",
  "message": "Artifact saved to /path/to/script.py"
}
```

### 3. `list_artifacts` - Lister les artifacts

Liste les artifacts créés avec filtres.

**Paramètres:**
```json
{
  "type_filter": "code",  // Optionnel
  "limit": 10             // Optionnel (défaut: 10)
}
```

**Réponse:**
```json
{
  "success": true,
  "artifacts": [
    {
      "id": "artifact_12345",
      "name": "script.py",
      "type": "code",
      "created_at": "2025-10-28T12:00:00Z"
    }
  ],
  "total": 1
}
```

### 4. `update_artifact` - Mettre à jour un artifact

Met à jour le contenu ou les métadonnées d'un artifact.

**Paramètres:**
```json
{
  "artifact_id": "artifact_12345",
  "content": "print('Hello World')",  // Optionnel
  "description": "Updated script",    // Optionnel
  "metadata": {"version": "2.0"}      // Optionnel
}
```

**Réponse:**
```json
{
  "success": true,
  "artifact_id": "artifact_12345",
  "updated_fields": ["content", "metadata"],
  "artifact": { /* artifact complet */ }
}
```

### 5. `delete_artifact` - Supprimer un artifact

Supprime un artifact du store.

**Paramètres:**
```json
{
  "artifact_id": "artifact_12345"
}
```

**Réponse:**
```json
{
  "success": true,
  "artifact_id": "artifact_12345",
  "message": "Artifact deleted"
}
```

## 📝 Types d'Artifacts

| Type | Description | Extensions | Langages supportés |
|------|-------------|-----------|-------------------|
| `code` | Code source | .py, .js, .ts, .java, .go, etc. | python, javascript, typescript, java, go, rust, etc. |
| `document` | Documents | .md, .txt, .html | markdown, html, plaintext |
| `data` | Données structurées | .json, .yaml, .toml, .csv | json, yaml, toml |
| `config` | Configurations | .env, .conf, .ini | - |

## 🚀 Utilisation via API

### Via FastAPI

```bash
# 1. Créer un artifact
curl -X POST http://localhost:8000/api/mcp/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "create_artifact",
    "arguments": {
      "name": "hello.py",
      "type": "code",
      "content": "def hello():\n    print(\"Hello World\")",
      "language": "python"
    }
  }'

# 2. Lister les artifacts
curl -X POST http://localhost:8000/api/mcp/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "list_artifacts",
    "arguments": {
      "type_filter": "code",
      "limit": 5
    }
  }'

# 3. Sauvegarder un artifact
curl -X POST http://localhost:8000/api/mcp/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "save_artifact",
    "arguments": {
      "artifact_id": "artifact_12345",
      "path": "./output/hello.py"
    }
  }'
```

### Via Client Python

```python
import httpx

async def create_and_save_artifact():
    async with httpx.AsyncClient() as client:
        # Créer
        response = await client.post(
            "http://localhost:8000/api/mcp/call",
            json={
                "tool": "create_artifact",
                "arguments": {
                    "name": "app.js",
                    "type": "code",
                    "content": "console.log('Hello');",
                    "language": "javascript"
                }
            }
        )
        artifact = response.json()["result"]["artifact"]
        artifact_id = artifact["id"]

        # Sauvegarder
        await client.post(
            "http://localhost:8000/api/mcp/call",
            json={
                "tool": "save_artifact",
                "arguments": {
                    "artifact_id": artifact_id,
                    "path": "./output/app.js"
                }
            }
        )
```

## 💡 Exemples d'Utilisation

### Exemple 1: Créer un script Python

```json
POST /api/mcp/call
{
  "tool": "create_artifact",
  "arguments": {
    "name": "data_processor.py",
    "type": "code",
    "content": "import pandas as pd\n\ndef process_data(df):\n    return df.dropna()",
    "description": "Script de traitement de données",
    "metadata": {
      "author": "AI Agent",
      "version": "1.0.0"
    }
  }
}
```

### Exemple 2: Créer un document Markdown

```json
POST /api/mcp/call
{
  "tool": "create_artifact",
  "arguments": {
    "name": "README.md",
    "type": "document",
    "content": "# Mon Projet\n\n## Description\n\nCe projet fait X, Y, Z.",
    "language": "markdown"
  }
}
```

### Exemple 3: Créer un fichier de configuration

```json
POST /api/mcp/call
{
  "tool": "create_artifact",
  "arguments": {
    "name": "config.json",
    "type": "data",
    "content": "{\"api_url\": \"https://api.example.com\", \"timeout\": 30}",
    "language": "json"
  }
}
```

## 🔄 Workflow Complet

```python
# 1. Créer un artifact
create_response = await mcp_call("create_artifact", {
    "name": "calculator.py",
    "type": "code",
    "content": "def add(a, b):\n    return a + b"
})

artifact_id = create_response["artifact"]["id"]

# 2. Mettre à jour l'artifact
await mcp_call("update_artifact", {
    "artifact_id": artifact_id,
    "content": "def add(a, b):\n    \"\"\"Additionne deux nombres.\"\"\"\n    return a + b"
})

# 3. Sauvegarder sur disque
await mcp_call("save_artifact", {
    "artifact_id": artifact_id,
    "path": "./src/calculator.py"
})

# 4. Lister tous les artifacts
artifacts = await mcp_call("list_artifacts", {})

# 5. Supprimer l'artifact (optionnel)
await mcp_call("delete_artifact", {
    "artifact_id": artifact_id
})
```

## 🎯 Cas d'Usage

### 1. Génération de Code

```python
# L'agent génère du code et le sauvegarde
code = """
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
"""

await create_artifact(
    name="user.py",
    type="code",
    content=code,
    language="python"
)
```

### 2. Documentation Automatique

```python
# L'agent génère de la documentation
doc = """
# API Documentation

## Endpoints

### GET /users
Returns all users

### POST /users
Creates a new user
"""

await create_artifact(
    name="API.md",
    type="document",
    content=doc
)
```

### 3. Configuration Dynamique

```python
# L'agent génère des fichiers de config
config = {
    "database": {
        "host": "localhost",
        "port": 5432
    }
}

await create_artifact(
    name="config.yaml",
    type="config",
    content=yaml.dump(config)
)
```

## 🔒 Limitations & Sécurité

### Limitations
- **Max artifacts**: 100 artifacts en mémoire (configurable)
- **Pas de persistence**: Les artifacts sont perdus au redémarrage (sauf export/import)
- **Taille max**: Limité par la mémoire disponible

### Sécurité
⚠️ **Important**:
- Ne pas sauvegarder dans des chemins système sensibles
- Valider tous les chemins avant sauvegarde
- Nettoyer régulièrement les artifacts obsolètes
- Ne pas stocker de données sensibles (passwords, tokens)

## 📊 Monitoring

### Obtenir les statistiques

```bash
# Via l'artifact store (backend)
from backend.mcp.artifact_store import artifact_store

stats = artifact_store.get_stats()
# {
#   "total_artifacts": 42,
#   "by_type": {"code": 30, "document": 10, "data": 2},
#   "total_size_bytes": 125000,
#   "max_artifacts": 100
# }
```

## 💾 Persistence

### Export vers fichier

```python
from backend.mcp.artifact_store import artifact_store

# Export
artifact_store.export_to_file("artifacts_backup.json")

# Import
artifact_store.import_from_file("artifacts_backup.json")
```

## 🧪 Tests

### Test unitaire

```python
import pytest
from backend.mcp.artifacts import create_artifact, save_artifact

@pytest.mark.asyncio
async def test_create_artifact():
    result = await create_artifact(
        name="test.py",
        type="code",
        content="print('test')"
    )

    assert result["success"] is True
    assert result["artifact"]["name"] == "test.py"
    assert result["artifact"]["type"] == "code"
```

## 🔗 Intégration avec Gemini

L'agent peut utiliser les artifacts via function calling :

```python
# Gemini appelle automatiquement create_artifact
response = await gemini.generate_with_tools(
    prompt="Crée un script Python qui affiche Hello World",
    tools=mcp_server.get_tools_schema()
)

# Gemini a appelé create_artifact automatiquement
function_call = response["function_calls"][0]
# {
#   "name": "create_artifact",
#   "arguments": {
#     "name": "hello.py",
#     "type": "code",
#     "content": "print('Hello World')"
#   }
# }
```

## 📚 Ressources

- **Code source**: `backend/mcp/artifacts.py`
- **Store**: `backend/mcp/artifact_store.py`
- **Schémas**: `backend/mcp/schemas.py`
- **Tests**: `tests/test_artifacts.py` (à créer)

---

✅ Le système d'artifacts est maintenant intégré comme **skill MCP** dans l'agent IA !
