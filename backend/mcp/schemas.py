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

# === REGISTRY ===

TOOL_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "search_memory": SEARCH_MEMORY_SCHEMA,
    "store_memory": STORE_MEMORY_SCHEMA,
    "analyze_sentiment": ANALYZE_SENTIMENT_SCHEMA,
    "extract_keywords": EXTRACT_KEYWORDS_SCHEMA,
    "calculate": CALCULATE_SCHEMA,
    "get_current_context": GET_CONTEXT_SCHEMA,
}
