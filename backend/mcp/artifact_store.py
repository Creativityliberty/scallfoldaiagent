"""
Store pour la gestion des artifacts.
Stockage en mémoire avec persistence optionnelle.
"""

from typing import Dict, Any, List
from datetime import datetime
from loguru import logger
import json
from pathlib import Path

class ArtifactStore:
    """Store centralisé pour les artifacts."""

    def __init__(self):
        self.artifacts: Dict[str, Dict[str, Any]] = {}
        self.max_artifacts = 100
        logger.info("ArtifactStore initialized")

    def add(self, artifact: Dict[str, Any]) -> str:
        """
        Ajoute un artifact au store.

        Args:
            artifact: Données de l'artifact

        Returns:
            ID de l'artifact
        """
        artifact_id = artifact["id"]

        # Limite le nombre d'artifacts
        if len(self.artifacts) >= self.max_artifacts:
            # Supprime le plus ancien
            oldest_id = min(
                self.artifacts.keys(),
                key=lambda k: self.artifacts[k].get("created_at", "")
            )
            del self.artifacts[oldest_id]
            logger.warning(f"Removed oldest artifact {oldest_id} (max limit reached)")

        self.artifacts[artifact_id] = artifact
        logger.info(f"Added artifact {artifact_id} to store")

        return artifact_id

    def get(self, artifact_id: str) -> Dict[str, Any] | None:
        """Récupère un artifact par son ID."""
        return self.artifacts.get(artifact_id)

    def list(
        self,
        type_filter: str | None = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Liste les artifacts avec filtres."""
        artifacts = list(self.artifacts.values())

        # Filtre par type
        if type_filter:
            artifacts = [a for a in artifacts if a.get("type") == type_filter]

        # Trie par date de création (plus récent d'abord)
        artifacts.sort(
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )

        return artifacts[:limit]

    def update(
        self,
        artifact_id: str,
        content: str | None = None,
        description: str | None = None,
        metadata: Dict[str, Any] | None = None
    ) -> Dict[str, Any] | None:
        """Met à jour un artifact."""
        artifact = self.get(artifact_id)

        if not artifact:
            return None

        if content is not None:
            artifact["content"] = content
            artifact["size_bytes"] = len(content.encode('utf-8'))
            artifact["lines"] = len(content.split('\n'))

        if description is not None:
            artifact["description"] = description

        if metadata is not None:
            artifact["metadata"].update(metadata)

        artifact["updated_at"] = datetime.now().isoformat()

        logger.info(f"Updated artifact {artifact_id}")

        return artifact

    def delete(self, artifact_id: str) -> bool:
        """Supprime un artifact."""
        if artifact_id in self.artifacts:
            del self.artifacts[artifact_id]
            logger.info(f"Deleted artifact {artifact_id}")
            return True

        return False

    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du store."""
        types = {}
        total_size = 0

        for artifact in self.artifacts.values():
            artifact_type = artifact.get("type", "unknown")
            types[artifact_type] = types.get(artifact_type, 0) + 1
            total_size += artifact.get("size_bytes", 0)

        return {
            "total_artifacts": len(self.artifacts),
            "by_type": types,
            "total_size_bytes": total_size,
            "max_artifacts": self.max_artifacts
        }

    def export_to_file(self, filepath: str) -> None:
        """Exporte tous les artifacts vers un fichier JSON."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.artifacts, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported {len(self.artifacts)} artifacts to {filepath}")

    def import_from_file(self, filepath: str) -> int:
        """Importe des artifacts depuis un fichier JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            imported = json.load(f)

        count = 0
        for artifact_id, artifact in imported.items():
            self.artifacts[artifact_id] = artifact
            count += 1

        logger.info(f"Imported {count} artifacts from {filepath}")

        return count

    def clear(self) -> None:
        """Vide le store."""
        count = len(self.artifacts)
        self.artifacts.clear()
        logger.info(f"Cleared {count} artifacts from store")


# Instance globale
artifact_store = ArtifactStore()
