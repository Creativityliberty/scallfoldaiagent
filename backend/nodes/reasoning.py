from typing import Dict, Any, List
from ..core.base_node import BaseNode
from ..core.shared import Shared
from ..llm.gemini_client import GeminiClient
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
    
    def __init__(self):
        super().__init__("reasoning")
        # Lazy: évite l'exigence de variables d'env pendant les tests
        self.gemini: Any | None = None
    
    def _ensure_client(self) -> None:
        if self.gemini is not None:
            return
        try:
            # Import tardif pour éviter la construction de Settings si non nécessaire
            from ..config import get_settings  # type: ignore
            settings = get_settings()
            self.gemini = GeminiClient(
                api_key=settings.gemini_api_key,
                model=settings.gemini_model,
            )
        except Exception as e:
            # Fallback env direct (utile en dev minimal ou tests avec mock)
            import os
            api_key = os.getenv("GEMINI_API_KEY")
            model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")
            if api_key:
                self.gemini = GeminiClient(api_key=api_key, model=model)
            else:
                # L'appelant peut injecter self.gemini (mock) avant usage
                logger.debug("Gemini client not configured; expecting mock or later injection.")

    def prep(self, shared: Shared) -> Dict[str, Any]:
        """Récupère le contexte nécessaire au raisonnement."""
        return {
            "intent": shared.get_result("interpretation", "intent"),
            "task_type": shared.get_result("interpretation", "task_type"),
            "clean_input": shared.get_result("perception", "clean_input"),
            "memory_context": shared.get_context("memory_snapshot", []),
        }
    
    async def exec(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute le cycle RRLA complet."""
        logger.info(f"Starting RRLA reasoning for intent: {input_data.get('intent')}")
        
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
            "reasoning_trace": self._build_trace(steps, evaluated_steps, logic_chain)
        }
    
    async def _decompose(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """R1: Décompose le problème en étapes."""
        prompt = f"""
Tu es un agent de raisonnement. Décompose cette requête en étapes logiques.

Requête: {context.get('clean_input','')}
Type de tâche: {context.get('task_type','')}
Intention: {context.get('intent','')}

Réponds en JSON avec cette structure:
{{
    "steps": [
        {{"id": 1, "action": "...", "rationale": "..."}},
        {{"id": 2, "action": "...", "rationale": "..."}}
    ]
}}
"""
        try:
            if self.gemini is None:
                self._ensure_client()
            if self.gemini is None:
                raise RuntimeError("Gemini client unavailable")
            response = await self.gemini.generate(prompt)
            data = json.loads(response)
            return data.get("steps", [])
        except Exception as e:
            logger.warning(f"RRLA decompose fallback due to error: {e}")
            return [{"id": 1, "action": "Répondre directement", "rationale": "Pas de décomposition nécessaire"}]
    
    async def _reflect(self, steps: List[Dict], context: Dict) -> List[Dict]:
        """R2: Évalue chaque étape."""
        for step in steps:
            step["feasibility"] = 0.8  # Simulation - à remplacer par un scoring réel
            step["priority"] = len(steps) - step["id"] + 1
        return steps
    
    async def _build_logic_chain(self, steps: List[Dict]) -> Dict[str, Any]:
        """L: Construit la chaîne logique d'exécution."""
        return {
            "sequence": [s["id"] for s in sorted(steps, key=lambda x: x.get("priority", 0), reverse=True)],
            "dependencies": {},
            "critical_path": [s["id"] for s in steps if s.get("feasibility", 0) > 0.7]
        }
    
    async def _decide(self, logic_chain: Dict, context: Dict) -> Dict[str, Any]:
        """A: Prend la décision finale."""
        return {
            "action_type": "generate_response",
            "confidence": 0.85,
            "next_steps": logic_chain["sequence"],
            "requires_tools": False
        }
    
    def _build_trace(self, steps, evaluated, chain) -> str:
        """Construit une trace lisible du raisonnement."""
        trace = "=== RRLA Reasoning Trace ===\n"
        trace += f"Decomposition: {len(steps)} steps\n"
        trace += f"Logic chain: {chain['sequence']}\n"
        return trace
