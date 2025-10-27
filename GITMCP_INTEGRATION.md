# 🔗 GitMCP Integration

Intégration complète de GitMCP pour charger le contexte des repos GitHub directement dans l'agent IA.

## 🎯 Fonctionnalités

- **URL GitHub → GitMCP**: Convertit automatiquement `github.com/user/repo` en `gitmcp.io/user/repo`
- **Fetch contexte**: Récupère `llms.txt`, `llms-full.txt`, et `README.md` du repo
- **Injection automatique**: Le contexte repo est injecté dans chaque message envoyé à l'agent
- **Statut visuel**: Indicateurs de chargement, succès, erreur en temps réel

## 🚀 Utilisation

### 1. Coller une URL GitHub

```
Exemples acceptés:
- github.com/user/repo
- https://github.com/user/repo
- github.com/user/repo.git
- username.github.io/repo
```

### 2. Cliquer sur "📦 Charger Repo"

Ou appuyer sur **Entrée** dans le champ URL.

### 3. Attendre le chargement

- ⏳ **Chargement...** : Requête en cours
- ✅ **Repo chargé** : Contexte disponible
- ❌ **Erreur** : Vérifier l'URL

### 4. Poser des questions

Une fois le repo chargé, chaque message inclura automatiquement:
```
[Contexte Repo: gitmcp.io/user/repo]
Votre question ici...
```

## 📦 Architecture Backend

### `backend/integrations/gitmcp.py`

```python
class GitMCPClient:
    # Normalise les URLs GitHub → GitMCP
    normalize_url(url: str) -> str
    
    # Récupère llms.txt, README, etc
    async fetch_context(repo_url: str) -> Dict[str, Any]
    
    # Extrait un résumé pour injection
    extract_summary(context: Dict) -> str
```

### Endpoint API

```
POST /api/gitmcp/fetch
{
  "url": "github.com/user/repo"
}

Response:
{
  "success": true,
  "url": "gitmcp.io/user/repo",
  "llms_context": "...",
  "readme": "...",
  "source": "gitmcp"
}
```

## 🎨 Frontend

### Éléments UI

- **Input GitMCP**: Champ pour coller l'URL
- **Bouton Charger**: Lance la requête
- **Statut**: Affiche l'état (loading/success/error/warning)
- **Message système**: Confirme le chargement du repo

### Styles CSS

```css
.gitmcp-section { /* Conteneur principal */ }
.gitmcp-status { /* Indicateur d'état */ }
.gitmcp-status.loading { /* Bleu */ }
.gitmcp-status.success { /* Vert */ }
.gitmcp-status.error { /* Rouge */ }
.gitmcp-status.warning { /* Orange */ }
.message.system { /* Messages système */ }
```

## 🔧 Configuration

### `.env`

```bash
GITMCP_ENABLED=true
```

### `backend/config.py`

```python
gitmcp_enabled: bool = True
```

## 📝 Flux d'exécution

```
1. Utilisateur colle URL GitHub
   ↓
2. Frontend normalise l'URL
   ↓
3. POST /api/gitmcp/fetch
   ↓
4. GitMCPClient.fetch_context()
   - Convertit en gitmcp.io
   - Fetch llms.txt (ou llms-full.txt)
   - Fetch README.md
   ↓
5. Retour au frontend
   ↓
6. Affiche statut ✅
   ↓
7. Stocke repoContext en mémoire
   ↓
8. Utilisateur pose une question
   ↓
9. Message injecté avec contexte repo
   ↓
10. Agent IA traite avec contexte
```

## 🛠️ Développement

### Ajouter un nouveau fichier à récupérer

```python
# backend/integrations/gitmcp.py
async def fetch_context(repo_url: str) -> Dict[str, Any]:
    # ...
    package_json = await GitMCPClient._fetch_file(client, gitmcp_url, "package.json")
    # ...
    return {
        "success": True,
        "package_json": package_json or "",
        # ...
    }
```

### Personnaliser le résumé injecté

```python
# backend/integrations/gitmcp.py
@staticmethod
def extract_summary(context: Dict[str, Any]) -> str:
    # Modifier le format du résumé ici
    summary = f"## Repository Context\n"
    # ...
    return summary
```

## ✅ Tests

```bash
# Tester la normalisation d'URL
python -c "from backend.integrations.gitmcp import GitMCPClient; print(GitMCPClient.normalize_url('github.com/user/repo'))"

# Tester le fetch (nécessite une URL valide)
python -c "
import asyncio
from backend.integrations.gitmcp import GitMCPClient
result = asyncio.run(GitMCPClient.fetch_context('github.com/torvalds/linux'))
print(result)
"
```

## 🐛 Troubleshooting

| Problème | Solution |
|----------|----------|
| ❌ Erreur 404 | Vérifier que le repo existe et est public |
| ⏳ Timeout | Repo trop volumineux ou réseau lent |
| ❌ Pas de llms.txt | Fallback sur llms-full.txt ou README |
| 🔒 Repo privé | GitMCP nécessite des repos publics |

## 📚 Ressources

- [GitMCP Documentation](https://gitmcp.io)
- [GitHub API Raw Content](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file)
- [Model Context Protocol](https://modelcontextprotocol.io)

## 🎯 Prochaines étapes

- [ ] Cacher le contexte repo dans la mémoire vectorielle
- [ ] Supporter les repos privés (avec token GitHub)
- [ ] Ajouter un cache local des repos
- [ ] Intégrer avec MCP tools pour appels directs
- [ ] Afficher les fichiers du repo dans un panneau latéral
