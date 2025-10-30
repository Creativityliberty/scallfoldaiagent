from typing import Dict, Any, List
from ..core.base_node import BaseNode
from ..core.shared import Shared
from ..llm.gemini_client import GeminiClient
from ..llm.prompt_builder import PromptBuilder
from ..config import get_settings
from loguru import logger
import json

class ReasoningNode(BaseNode):
    """
    Module 3: Raisonnement (RRLA)
    - R: Raisonnement (décomposition du problème)
    - R: Réflexion (évaluation des options)
    - L: Logique (chaînage d'inférences)
    - A: Action (décision)
    """

    def __init__(self) -> None:
        super().__init__("reasoning")
        self.settings = get_settings()
        self.gemini = GeminiClient(
            api_key=self.settings.gemini_api_key,
            model=self.settings.gemini_model
        )
        self.prompt_builder = PromptBuilder()

    def prep(self, shared: Shared) -> Dict[str, Any]:
        """Récupère le contexte nécessaire au raisonnement."""
        return {
            "intent": shared.get_result("interpretation", "intent"),
            "task_type": shared.get_result("interpretation", "task_type"),
            "clean_input": shared.get_result("perception", "clean_input"),
            "memory_context": shared.get_context("memory_snapshot", []),
            "complexity": shared.get_result("interpretation", "complexity")
        }

    async def exec(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute le cycle RRLA complet."""
        logger.info(f"Starting RRLA reasoning for intent: {input_data['intent']}")

        # Pour les tâches simples, skip le RRLA complet
        if input_data.get("complexity") == "simple":
            return await self._simple_reasoning(input_data)

        # R1: Raisonnement - Décomposition
        steps = await self._decompose(input_data)

        # R2: Réflexion - Évaluation
        evaluated_steps = await self._reflect(steps, input_data)

        # L: Logique - Chaînage
        logic_chain = await self._build_logic_chain(evaluated_steps)

        # A: Action - Décision
        decision = await self._decide(logic_chain, input_data)

        return {
            "steps": steps,
            "evaluated_steps": evaluated_steps,
            "logic_chain": logic_chain,
            "decision": decision,
            "confidence": decision.get("confidence", 0.5),
            "reasoning_trace": self._build_trace(steps, evaluated_steps, logic_chain),
            "mode": "full_rrla"
        }

    async def _simple_reasoning(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Raisonnement simplifié pour tâches basiques."""
        return {
            "steps": [{"id": 1, "action": "Répondre directement", "rationale": "Tâche simple"}],
            "evaluated_steps": [],
            "logic_chain": {"sequence": [1]},
            "decision": {
                "action_type": "generate_response",
                "confidence": 0.8,
                "next_steps": [1],
                "requires_tools": False
            },
            "confidence": 0.8,
            "reasoning_trace": "Simple reasoning: direct response",
            "mode": "simple"
        }

    async def _decompose(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """R1: Décompose le problème en étapes."""
        prompt = self.prompt_builder.build_rrla_decompose(context)

        try:
            response = await self.gemini.generate(prompt, temperature=0.7)
            data = json.loads(response)
            return data.get("steps", [])
        except json.JSONDecodeError:
            logger.warning("Failed to parse RRLA decompose response, using fallback")
            return [{"id": 1, "action": "Répondre directement", "rationale": "Pas de décomposition nécessaire"}]
        except Exception as e:
            logger.error(f"RRLA decompose error: {e}")
            return [{"id": 1, "action": "Traiter la requête", "rationale": "Erreur de décomposition"}]

    async def _reflect(self, steps: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """R2: Évalue chaque étape."""
        # Évaluation simplifiée (peut être améliorée avec un appel LLM)
        for i, step in enumerate(steps):
            step["feasibility"] = 0.8 - (i * 0.1)  # Décroît légèrement
            step["priority"] = len(steps) - i  # Priorité inverse
            step["risks"] = []

        return steps

    async def _build_logic_chain(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """L: Construit la chaîne logique d'exécution."""
        # Trie par priorité
        sorted_steps = sorted(steps, key=lambda x: x.get("priority", 0), reverse=True)

        return {
            "sequence": [s["id"] for s in sorted_steps],
            "dependencies": {},
            "critical_path": [s["id"] for s in steps if s.get("feasibility", 0) > 0.7],
            "parallel_eligible": []
        }

    async def _decide(self, logic_chain: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """A: Prend la décision finale."""
        task_type = context.get("task_type", "general")

        requires_tools = task_type in ["code_generation", "data_analysis"]

        return {
            "action_type": "generate_response",
            "confidence": 0.85,
            "next_steps": logic_chain["sequence"],
            "requires_tools": requires_tools,
            "recommended_tools": [] if not requires_tools else ["search_memory"],
            "execution_strategy": "sequential"
        }

    def _build_trace(
        self,
        steps: List[Dict[str, Any]],
        evaluated: List[Dict[str, Any]],
        chain: Dict[str, Any]
    ) -> str:
        """Construit une trace lisible du raisonnement."""
        trace = "=== RRLA Reasoning Trace ===\n"
        trace += f"Decomposition: {len(steps)} steps\n"

        for step in steps:
            trace += f"  {step['id']}. {step.get('action', 'N/A')} "
            trace += f"(feasibility: {step.get('feasibility', 0):.2f})\n"

        trace += f"\nLogic chain: {chain['sequence']}\n"
        trace += f"Critical path: {chain['critical_path']}\n"

        return trace
