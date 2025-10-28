from ..core.base_node import BaseNode
from ..core.shared import Shared
from typing import Dict, Any
from loguru import logger

class ActionNode(BaseNode):
    """
    Module 6: Action
    Produit la réponse finale et gère les actions post-génération.
    """

    def __init__(self) -> None:
        super().__init__("action")

    def prep(self, shared: Shared) -> Dict[str, Any]:
        """Récupère la synthèse."""
        return {
            "synthesis": shared.get_result("synthesis"),
            "reasoning": shared.get_result("reasoning"),
            "interpretation": shared.get_result("interpretation")
        }

    async def exec(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formate et finalise la réponse."""
        synthesis = input_data["synthesis"]

        if not synthesis:
            logger.error("No synthesis available for action")
            return {
                "final": "Désolé, je n'ai pas pu générer de réponse.",
                "format": "text",
                "status": "error"
            }

        # Réponse finale
        final_response = synthesis.get("draft", "")

        # Post-traitement
        final_response = self._post_process(final_response)

        # Actions additionnelles
        actions_taken = self._execute_actions(input_data)

        return {
            "final": final_response,
            "format": "text",
            "actions_taken": actions_taken,
            "status": "completed",
            "metadata": {
                "confidence": synthesis.get("confidence", 0.0),
                "sources": synthesis.get("sources", []),
                "reasoning_summary": synthesis.get("reasoning_summary", "")
            }
        }

    def _post_process(self, text: str) -> str:
        """Post-traite la réponse."""
        # Nettoyage basique
        text = text.strip()

        # Enlève les balises markdown inutiles si présentes
        if text.startswith("```") and text.endswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])

        return text

    def _execute_actions(self, input_data: Dict[str, Any]) -> list[str]:
        """Exécute des actions post-génération si nécessaire."""
        actions = []

        reasoning = input_data.get("reasoning", {})
        decision = reasoning.get("decision", {})

        # Si des outils étaient requis
        if decision.get("requires_tools"):
            actions.append("tools_called")

        # Logging pour analytics
        actions.append("response_logged")

        return actions
