from ..core.base_node import BaseNode
from ..core.shared import Shared
from ..llm.gemini_client import GeminiClient
from ..llm.prompt_builder import PromptBuilder
from ..config import get_settings
from typing import Dict, Any
from loguru import logger

class SynthesisNode(BaseNode):
    """
    Module 5: Synthèse
    Agrège les résultats du raisonnement et génère une réponse structurée.
    """

    def __init__(self) -> None:
        super().__init__("synthesis")
        self.settings = get_settings()
        self.gemini = GeminiClient(
            api_key=self.settings.gemini_api_key,
            model=self.settings.gemini_model
        )
        self.prompt_builder = PromptBuilder()

    def prep(self, shared: Shared) -> Dict[str, Any]:
        """Récupère les résultats du raisonnement."""
        return {
            "reasoning": shared.get_result("reasoning"),
            "input": shared.get_result("perception", "clean_input"),
            "interpretation": shared.get_result("interpretation"),
            "memory_context": shared.get_context("memory_snapshot", [])
        }

    async def exec(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthétise une réponse complète."""
        reasoning = input_data["reasoning"]
        user_input = input_data["input"]

        logger.info(f"Synthesizing response (mode: {reasoning.get('mode', 'unknown')})")

        # Génération de la réponse via Gemini
        prompt = self.prompt_builder.build_synthesis(reasoning, user_input)

        try:
            response_text = await self.gemini.generate(
                prompt,
                temperature=0.7,
                max_output_tokens=1024
            )

            return {
                "draft": response_text,
                "sources": self._extract_sources(input_data),
                "confidence": reasoning.get("confidence", 0.5),
                "reasoning_summary": self._summarize_reasoning(reasoning),
                "metadata": {
                    "steps_count": len(reasoning.get("steps", [])),
                    "mode": reasoning.get("mode", "unknown"),
                    "task_type": input_data.get("interpretation", {}).get("task_type", "general")
                }
            }

        except Exception as e:
            logger.error(f"Synthesis generation error: {e}")
            return {
                "draft": "Je rencontre une difficulté pour générer la réponse. Pouvez-vous reformuler ?",
                "sources": [],
                "confidence": 0.3,
                "error": str(e)
            }

    def _extract_sources(self, input_data: Dict[str, Any]) -> list[Dict[str, str]]:
        """Extrait les sources utilisées."""
        sources = []

        # Ajouter les sources mémoire si présentes
        memory_context = input_data.get("memory_context", [])
        if memory_context:
            sources.append({
                "type": "memory",
                "count": len(memory_context),
                "description": "Contexte conversationnel"
            })

        return sources

    def _summarize_reasoning(self, reasoning: Dict[str, Any]) -> str:
        """Résume le processus de raisonnement."""
        mode = reasoning.get("mode", "unknown")

        if mode == "simple":
            return "Raisonnement direct"

        steps = reasoning.get("steps", [])
        if not steps:
            return "Pas de raisonnement structuré"

        summary = f"Raisonnement en {len(steps)} étapes"
        if reasoning.get("decision"):
            decision = reasoning["decision"]
            summary += f" → {decision.get('action_type', 'unknown action')}"

        return summary
