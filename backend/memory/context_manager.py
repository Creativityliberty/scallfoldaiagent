from typing import List, Dict, Any
from datetime import datetime
from loguru import logger

class ContextManager:
    """
    Gestionnaire de contexte conversationnel.
    Maintient l'historique et gère la fenêtre de contexte.
    """

    def __init__(self, max_length: int = 8000):
        self.max_length = max_length
        self.history: List[Dict[str, Any]] = []
        self.session_metadata: Dict[str, Any] = {
            "session_id": None,
            "user_id": None,
            "start_time": datetime.now().isoformat()
        }
        logger.info(f"ContextManager initialized (max_length={max_length})")

    def add_turn(
        self,
        role: str,
        content: str,
        metadata: Dict[str, Any] | None = None
    ) -> None:
        """Ajoute un tour de conversation."""
        turn = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        self.history.append(turn)
        logger.debug(f"Added turn: {role} ({len(content)} chars)")

        # Tronque si nécessaire
        self._truncate_if_needed()

    def get_recent_history(self, n_turns: int = 10) -> List[Dict[str, Any]]:
        """Récupère les N derniers tours."""
        return self.history[-n_turns:]

    def get_full_context(self) -> str:
        """Construit le contexte complet sous forme de texte."""
        context_parts = []

        for turn in self.history:
            role = turn["role"]
            content = turn["content"]
            context_parts.append(f"{role.upper()}: {content}")

        return "\n\n".join(context_parts)

    def get_token_count_estimate(self) -> int:
        """Estime le nombre de tokens dans le contexte."""
        # Approximation : 1 token ≈ 4 caractères
        full_context = self.get_full_context()
        return len(full_context) // 4

    def _truncate_if_needed(self) -> None:
        """Tronque l'historique si la limite est dépassée."""
        while self.get_token_count_estimate() > self.max_length:
            if len(self.history) <= 2:
                # Garde au moins 2 tours
                break

            # Supprime le tour le plus ancien (sauf le premier system message si présent)
            if self.history[0]["role"] == "system":
                self.history.pop(1)
            else:
                self.history.pop(0)

            logger.debug("Truncated history to fit max_length")

    def summarize_old_context(self) -> str:
        """Résume l'ancien contexte (pour compression)."""
        if len(self.history) < 5:
            return ""

        # Résumé basique des N premiers tours
        old_turns = self.history[:5]
        summary_parts = []

        for turn in old_turns:
            role = turn["role"]
            content = turn["content"][:100]  # Premiers 100 chars
            summary_parts.append(f"{role}: {content}...")

        return "Contexte précédent: " + " | ".join(summary_parts)

    def clear(self) -> None:
        """Vide l'historique."""
        self.history.clear()
        logger.info("Context cleared")

    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du contexte."""
        return {
            "total_turns": len(self.history),
            "estimated_tokens": self.get_token_count_estimate(),
            "max_length": self.max_length,
            "session_metadata": self.session_metadata
        }

    def export_history(self) -> List[Dict[str, Any]]:
        """Exporte l'historique complet."""
        return self.history.copy()
