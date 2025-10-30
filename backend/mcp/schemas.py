"""
Schémas JSON pour les outils MCP.
Définit les structures de données pour l'interface avec Gemini.
"""

from typing import Dict, Any

# === MEMORY SCHEMAS ===

SEARCH_MEMORY_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "Requête de recherche sémantique dans la mémoire"
        },
        "top_k": {
            "type": "integer",
            "description": "Nombre de résultats à retourner",
            "default": 5,
            "minimum": 1,
            "maximum": 20
        }
    },
    "required": ["query"]
}

STORE_MEMORY_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "content": {
            "type": "string",
            "description": "Contenu à stocker en mémoire"
        },
        "metadata": {
            "type": "object",
            "description": "Métadonnées optionnelles (tags, source, etc.)",
            "properties": {
                "tags": {"type": "array", "items": {"type": "string"}},
                "source": {"type": "string"},
                "importance": {"type": "number", "minimum": 0, "maximum": 1}
            }
        }
    },
    "required": ["content"]
}

# === ANALYSIS SCHEMAS ===

ANALYZE_SENTIMENT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string",
            "description": "Texte dont on veut analyser le sentiment"
        }
    },
    "required": ["text"]
}

EXTRACT_KEYWORDS_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string",
            "description": "Texte dont on veut extraire les mots-clés"
        },
        "max_keywords": {
            "type": "integer",
            "description": "Nombre maximum de mots-clés à extraire",
            "default": 10,
            "minimum": 1,
            "maximum": 50
        }
    },
    "required": ["text"]
}

# === UTILITY SCHEMAS ===

CALCULATE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "expression": {
            "type": "string",
            "description": "Expression mathématique à évaluer (ex: '2 + 2', '3 * 4 + 5')"
        }
    },
    "required": ["expression"]
}

GET_CONTEXT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {},
    "description": "Récupère le contexte actuel de l'agent (pas de paramètres requis)"
}

# === ARTIFACT SCHEMAS ===

CREATE_ARTIFACT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Nom de l'artifact (ex: 'script.py', 'document.md')"
        },
        "type": {
            "type": "string",
            "description": "Type d'artifact",
            "enum": ["code", "document", "data", "config"]
        },
        "content": {
            "type": "string",
            "description": "Contenu de l'artifact"
        },
        "language": {
            "type": "string",
            "description": "Langage de programmation (pour type='code')",
            "enum": ["python", "javascript", "typescript", "java", "go", "rust", "html", "css", "markdown"]
        },
        "description": {
            "type": "string",
            "description": "Description de l'artifact"
        },
        "metadata": {
            "type": "object",
            "description": "Métadonnées additionnelles"
        }
    },
    "required": ["name", "type", "content"]
}

SAVE_ARTIFACT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "artifact_id": {
            "type": "string",
            "description": "ID de l'artifact à sauvegarder"
        },
        "path": {
            "type": "string",
            "description": "Chemin de destination"
        },
        "create_dirs": {
            "type": "boolean",
            "description": "Créer les dossiers parents si nécessaire",
            "default": True
        }
    },
    "required": ["artifact_id", "path"]
}

LIST_ARTIFACTS_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "type_filter": {
            "type": "string",
            "description": "Filtrer par type d'artifact",
            "enum": ["code", "document", "data", "config"]
        },
        "limit": {
            "type": "integer",
            "description": "Nombre maximum de résultats",
            "default": 10,
            "minimum": 1,
            "maximum": 100
        }
    }
}

UPDATE_ARTIFACT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "artifact_id": {
            "type": "string",
            "description": "ID de l'artifact à mettre à jour"
        },
        "content": {
            "type": "string",
            "description": "Nouveau contenu (optionnel)"
        },
        "description": {
            "type": "string",
            "description": "Nouvelle description (optionnel)"
        },
        "metadata": {
            "type": "object",
            "description": "Nouvelles métadonnées (optionnel)"
        }
    },
    "required": ["artifact_id"]
}

DELETE_ARTIFACT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "artifact_id": {
            "type": "string",
            "description": "ID de l'artifact à supprimer"
        }
    },
    "required": ["artifact_id"]
}

# === REGISTRY ===

TOOL_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "search_memory": SEARCH_MEMORY_SCHEMA,
    "store_memory": STORE_MEMORY_SCHEMA,
    "analyze_sentiment": ANALYZE_SENTIMENT_SCHEMA,
    "extract_keywords": EXTRACT_KEYWORDS_SCHEMA,
    "calculate": CALCULATE_SCHEMA,
    "get_current_context": GET_CONTEXT_SCHEMA,
    # Artifacts
    "create_artifact": CREATE_ARTIFACT_SCHEMA,
    "save_artifact": SAVE_ARTIFACT_SCHEMA,
    "list_artifacts": LIST_ARTIFACTS_SCHEMA,
    "update_artifact": UPDATE_ARTIFACT_SCHEMA,
    "delete_artifact": DELETE_ARTIFACT_SCHEMA,
}
