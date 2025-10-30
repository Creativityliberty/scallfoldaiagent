from typing import Any, Dict
from pydantic import BaseModel, Field, validator
import re

class ChatRequest(BaseModel):
    """Validation d'une requête de chat."""
    input: str = Field(..., min_length=1, max_length=10000, description="Message utilisateur")
    user_id: str | None = Field(default="anonymous", description="ID de l'utilisateur")
    session_id: str | None = Field(default=None, description="ID de session")
    context: Dict[str, Any] | None = Field(default=None, description="Contexte additionnel")

    @validator('input')
    def validate_input(cls, v: str) -> str:
        """Valide et nettoie l'input."""
        # Trim whitespace
        v = v.strip()

        # Vérifie qu'il reste quelque chose
        if not v:
            raise ValueError("Input cannot be empty")

        # Limite les répétitions excessives de caractères
        if re.search(r'(.)\1{50,}', v):
            raise ValueError("Input contains excessive character repetition")

        return v

    @validator('user_id')
    def validate_user_id(cls, v: str | None) -> str:
        """Valide l'user_id."""
        if v and not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("Invalid user_id format")
        return v or "anonymous"

class MCPCallRequest(BaseModel):
    """Validation d'un appel MCP."""
    tool: str = Field(..., min_length=1, description="Nom de l'outil MCP")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments de l'outil")

    @validator('tool')
    def validate_tool_name(cls, v: str) -> str:
        """Valide le nom de l'outil."""
        if not re.match(r'^[a-z_][a-z0-9_]*$', v):
            raise ValueError("Tool name must be lowercase alphanumeric with underscores")
        return v

class StreamRequest(BaseModel):
    """Validation d'une requête de streaming."""
    prompt: str = Field(..., min_length=1, max_length=5000, description="Prompt pour le streaming")

    @validator('prompt')
    def validate_prompt(cls, v: str) -> str:
        """Valide le prompt."""
        v = v.strip()
        if not v:
            raise ValueError("Prompt cannot be empty")
        return v

def validate_confidence(confidence: float) -> float:
    """
    Valide une valeur de confiance.

    Args:
        confidence: Valeur à valider

    Returns:
        Valeur validée (entre 0 et 1)

    Raises:
        ValueError: Si la valeur est invalide
    """
    if not isinstance(confidence, (int, float)):
        raise ValueError("Confidence must be a number")

    if not 0 <= confidence <= 1:
        raise ValueError("Confidence must be between 0 and 1")

    return float(confidence)

def validate_token_count(tokens: int, max_tokens: int = 100000) -> int:
    """
    Valide un nombre de tokens.

    Args:
        tokens: Nombre de tokens
        max_tokens: Maximum autorisé

    Returns:
        Nombre de tokens validé

    Raises:
        ValueError: Si le nombre est invalide
    """
    if not isinstance(tokens, int):
        raise ValueError("Token count must be an integer")

    if tokens < 0:
        raise ValueError("Token count cannot be negative")

    if tokens > max_tokens:
        raise ValueError(f"Token count exceeds maximum ({max_tokens})")

    return tokens

def sanitize_html(text: str) -> str:
    """
    Nettoie le HTML d'un texte (basique).
    
    WARNING: This is a basic sanitization function. For production use,
    consider using a proper HTML parser like 'bleach' or 'html.parser'.
    Regex-based HTML sanitization can miss edge cases.

    Args:
        text: Texte à nettoyer

    Returns:
        Texte nettoyé
    """
    # Remove JavaScript blocks - handle whitespace in closing tags
    text = re.sub(r'<script[^>]*>.*?</script\s*>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove inline JavaScript event handlers
    text = re.sub(r'on\w+\s*=\s*["\'].*?["\']', '', text, flags=re.IGNORECASE)
    
    # Remove HTML tags (done last to catch any remaining tags)
    text = re.sub(r'<[^>]+>', '', text)

    return text.strip()

def validate_json_structure(data: Any, required_keys: list[str]) -> bool:
    """
    Valide qu'un dict contient les clés requises.

    Args:
        data: Données à valider
        required_keys: Liste des clés requises

    Returns:
        True si valide

    Raises:
        ValueError: Si des clés manquent
    """
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")

    missing = [key for key in required_keys if key not in data]

    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    return True
