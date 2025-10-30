"""
Exemple d'utilisation du système Artifacts via MCP.

Démontre comment créer, gérer et sauvegarder des artifacts.
"""

import asyncio
import httpx
from pathlib import Path

API_URL = "http://localhost:8000"

async def mcp_call(tool: str, arguments: dict) -> dict:
    """
    Appelle un outil MCP via l'API.

    Args:
        tool: Nom de l'outil
        arguments: Arguments de l'outil

    Returns:
        Résultat de l'appel
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/api/mcp/call",
            json={"tool": tool, "arguments": arguments}
        )
        return response.json()

async def demo_create_python_script():
    """Démo: Créer un script Python."""
    print("\n=== Création d'un script Python ===")

    code = """#!/usr/bin/env python3
\"\"\"Script de traitement de données.\"\"\"

import pandas as pd

def process_csv(filepath: str) -> pd.DataFrame:
    \"\"\"Traite un fichier CSV.\"\"\"
    df = pd.read_csv(filepath)
    df = df.dropna()
    df = df.drop_duplicates()
    return df

if __name__ == "__main__":
    result = process_csv("data.csv")
    print(f"Processed {len(result)} rows")
"""

    result = await mcp_call(
        "create_artifact",
        {
            "name": "data_processor.py",
            "type": "code",
            "content": code,
            "description": "Script de traitement de données CSV",
            "metadata": {
                "author": "AI Agent",
                "version": "1.0.0",
                "dependencies": ["pandas"]
            }
        }
    )

    if result["success"]:
        artifact = result["result"]["artifact"]
        print(f"✅ Artifact créé: {artifact['id']}")
        print(f"   Nom: {artifact['name']}")
        print(f"   Lignes: {artifact['lines']}")
        print(f"   Taille: {artifact['size_bytes']} bytes")
        return artifact["id"]
    else:
        print(f"❌ Erreur: {result.get('error')}")
        return None

async def demo_create_documentation():
    """Démo: Créer de la documentation."""
    print("\n=== Création de documentation ===")

    doc = """# Data Processor

## Description

Script Python pour le traitement de fichiers CSV.

## Installation

```bash
pip install pandas
```

## Usage

```python
from data_processor import process_csv

df = process_csv("mon_fichier.csv")
```

## Fonctionnalités

- ✅ Suppression des lignes vides
- ✅ Suppression des doublons
- ✅ Validation des données

## Licence

MIT License
"""

    result = await mcp_call(
        "create_artifact",
        {
            "name": "README.md",
            "type": "document",
            "content": doc
        }
    )

    if result["success"]:
        artifact = result["result"]["artifact"]
        print(f"✅ Documentation créée: {artifact['id']}")
        return artifact["id"]
    else:
        print(f"❌ Erreur: {result.get('error')}")
        return None

async def demo_create_config():
    """Démo: Créer un fichier de configuration."""
    print("\n=== Création de configuration ===")

    config = """{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "mydb",
    "pool_size": 10
  },
  "api": {
    "base_url": "https://api.example.com",
    "timeout": 30,
    "retry_attempts": 3
  },
  "logging": {
    "level": "INFO",
    "format": "json",
    "output": "logs/app.log"
  }
}"""

    result = await mcp_call(
        "create_artifact",
        {
            "name": "config.json",
            "type": "config",
            "content": config,
            "language": "json"
        }
    )

    if result["success"]:
        artifact = result["result"]["artifact"]
        print(f"✅ Configuration créée: {artifact['id']}")
        return artifact["id"]
    else:
        print(f"❌ Erreur: {result.get('error')}")
        return None

async def demo_list_artifacts():
    """Démo: Lister tous les artifacts."""
    print("\n=== Liste des artifacts ===")

    result = await mcp_call(
        "list_artifacts",
        {"limit": 10}
    )

    if result["success"]:
        artifacts = result["result"]["artifacts"]
        print(f"📦 Total: {len(artifacts)} artifacts\n")

        for artifact in artifacts:
            print(f"  • {artifact['name']}")
            print(f"    ID: {artifact['id']}")
            print(f"    Type: {artifact['type']}")
            print(f"    Créé: {artifact['created_at']}")
            print()

async def demo_update_artifact(artifact_id: str):
    """Démo: Mettre à jour un artifact."""
    print(f"\n=== Mise à jour de l'artifact {artifact_id} ===")

    result = await mcp_call(
        "update_artifact",
        {
            "artifact_id": artifact_id,
            "description": "Script de traitement de données CSV (version améliorée)",
            "metadata": {
                "version": "2.0.0",
                "updated_by": "AI Agent"
            }
        }
    )

    if result["success"]:
        print(f"✅ Artifact mis à jour")
        print(f"   Champs modifiés: {result['result']['updated_fields']}")
    else:
        print(f"❌ Erreur: {result.get('error')}")

async def demo_save_to_disk(artifact_id: str, path: str):
    """Démo: Sauvegarder un artifact sur disque."""
    print(f"\n=== Sauvegarde de {artifact_id} ===")

    result = await mcp_call(
        "save_artifact",
        {
            "artifact_id": artifact_id,
            "path": path,
            "create_dirs": True
        }
    )

    if result["success"]:
        saved_path = result["result"]["path"]
        print(f"✅ Sauvegardé dans: {saved_path}")

        # Vérifie que le fichier existe
        if Path(saved_path).exists():
            print(f"   ✓ Fichier créé avec succès")
    else:
        print(f"❌ Erreur: {result.get('error')}")

async def demo_workflow_complet():
    """Démo complète du workflow artifacts."""
    print("=" * 60)
    print("🎨 Démonstration Complète - Artifacts Skill MCP")
    print("=" * 60)

    try:
        # 1. Créer des artifacts
        script_id = await demo_create_python_script()
        doc_id = await demo_create_documentation()
        config_id = await demo_create_config()

        # 2. Lister
        await demo_list_artifacts()

        # 3. Mettre à jour
        if script_id:
            await demo_update_artifact(script_id)

        # 4. Sauvegarder sur disque
        output_dir = Path("./output_artifacts")
        output_dir.mkdir(exist_ok=True)

        if script_id:
            await demo_save_to_disk(script_id, str(output_dir / "data_processor.py"))
        if doc_id:
            await demo_save_to_disk(doc_id, str(output_dir / "README.md"))
        if config_id:
            await demo_save_to_disk(config_id, str(output_dir / "config.json"))

        print("\n" + "=" * 60)
        print("✅ Démonstration terminée avec succès !")
        print(f"📂 Fichiers sauvegardés dans: {output_dir.absolute()}")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erreur pendant la démonstration: {e}")

async def main():
    """Point d'entrée principal."""
    print("\n🚀 Démarrage de la démonstration...\n")

    # Vérifie que l'API est accessible
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/health")
            if response.status_code == 200:
                print("✅ API accessible")
            else:
                print("⚠️  API répond mais statut inhabituel")
    except Exception as e:
        print(f"❌ Impossible de se connecter à l'API: {e}")
        print(f"   Assurez-vous que le serveur tourne sur {API_URL}")
        return

    # Lance la démo
    await demo_workflow_complet()

if __name__ == "__main__":
    asyncio.run(main())
