from ..core.base_node import BaseNode
from ..core.shared import Shared
from typing import Dict, Any
import re

class PerceptionNode(BaseNode):
    """
    Module 1: Perception
    Nettoie et normalise l'entrée utilisateur.
    """

    def __init__(self) -> None:
        super().__init__("perception")

    async def exec(self, input_data: Any) -> Dict[str, Any]:
        """Nettoie et structure l'input utilisateur."""
        raw_input = input_data or ""

        # Nettoyage basique
        clean_input = raw_input.strip()
        clean_input = re.sub(r'\s+', ' ', clean_input)  # Normalise les espaces

        # Détection de patterns
        has_question = '?' in clean_input
        has_command = any(clean_input.lower().startswith(cmd) for cmd in [
            'fais', 'crée', 'génère', 'écris', 'explique', 'analyse'
        ])

        return {
            "raw": raw_input,
            "clean_input": clean_input,
            "length": len(clean_input),
            "has_question": has_question,
            "has_command": has_command,
            "language": self._detect_language(clean_input)
        }

    def _detect_language(self, text: str) -> str:
        """Détection simple de la langue."""
        french_markers = ['le', 'la', 'les', 'un', 'une', 'des', 'est', 'sont', 'quel', 'comment']
        english_markers = ['the', 'a', 'an', 'is', 'are', 'what', 'how', 'can', 'will']

        text_lower = text.lower()
        french_count = sum(1 for marker in french_markers if f' {marker} ' in f' {text_lower} ')
        english_count = sum(1 for marker in english_markers if f' {marker} ' in f' {text_lower} ')

        if french_count > english_count:
            return "fr"
        elif english_count > french_count:
            return "en"
        return "unknown"
