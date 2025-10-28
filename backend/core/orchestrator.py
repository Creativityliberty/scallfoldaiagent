from typing import Dict, Any
from loguru import logger

from .shared import Shared
from ..nodes.perception import PerceptionNode
from ..nodes.interpretation import InterpretationNode
from ..nodes.memory import MemoryNode
from ..nodes.reasoning import ReasoningNode
from ..nodes.synthesis import SynthesisNode
from ..nodes.action import ActionNode

class Orchestrator:
    """
    Orchestrateur PocketFlow central.
    Coordonne l'exécution séquentielle des nodes avec gestion d'erreurs.
    """

    def __init__(self):
        # Pipeline de nodes
        self.pipeline = [
            PerceptionNode(),
            InterpretationNode(),
            MemoryNode(),
            ReasoningNode(),
            SynthesisNode(),
            ActionNode(),
        ]
        logger.info(f"Orchestrator initialized with {len(self.pipeline)} nodes")

    async def run(self, shared: Shared) -> Dict[str, Any]:
        """Exécute le flow complet."""
        flow_id = shared.get_metadata('flow_id')
        logger.info(f"Starting flow {flow_id}")

        input_data = shared.get_context("user_input")

        for node in self.pipeline:
            try:
                logger.debug(f"Executing node: {node.name}")
                result, next_route = await node.run(shared, input_data)
                input_data = result

                # Gestion du routage conditionnel (si implémenté)
                if next_route:
                    logger.info(f"Routing to: {next_route}")
                    # Logique de routage personnalisée
                    # Peut être étendue pour supporter des flows conditionnels

            except Exception as e:
                logger.error(f"Node {node.name} failed: {e}", exc_info=True)
                # Stratégie de fallback
                shared.set_result(node.name, {"error": str(e)})

                # Décide si on continue ou on arrête
                if self._is_critical_node(node.name):
                    logger.error(f"Critical node {node.name} failed, stopping flow")
                    break
                else:
                    logger.warning(f"Non-critical node {node.name} failed, continuing")

        # Résultat final
        final_result = shared.get_result("action")

        return {
            "answer": final_result.get("final") if final_result else "Erreur de traitement",
            "confidence": shared.get_result("reasoning", {}).get("confidence") or 0.0,
            "metadata": shared["metadata"],
            "trace": shared.get_trace(),
            "status": "completed" if final_result else "error"
        }

    def _is_critical_node(self, node_name: str) -> bool:
        """Détermine si un node est critique pour le flow."""
        critical_nodes = ["perception", "interpretation"]
        return node_name in critical_nodes

    async def run_partial(
        self,
        shared: Shared,
        start_node: str | None = None,
        end_node: str | None = None
    ) -> Dict[str, Any]:
        """Exécute une partie du pipeline."""
        start_idx = 0
        end_idx = len(self.pipeline)

        # Trouve les indices
        if start_node:
            for i, node in enumerate(self.pipeline):
                if node.name == start_node:
                    start_idx = i
                    break

        if end_node:
            for i, node in enumerate(self.pipeline):
                if node.name == end_node:
                    end_idx = i + 1
                    break

        logger.info(f"Running partial flow from {start_node} to {end_node}")

        input_data = shared.get_context("user_input")

        for node in self.pipeline[start_idx:end_idx]:
            try:
                result, _ = await node.run(shared, input_data)
                input_data = result
            except Exception as e:
                logger.error(f"Node {node.name} failed in partial run: {e}")
                break

        return {
            "status": "partial_completed",
            "results": shared["results"]
        }

    def get_pipeline_info(self) -> Dict[str, Any]:
        """Retourne les informations sur le pipeline."""
        return {
            "nodes": [
                {
                    "name": node.name,
                    "type": node.__class__.__name__
                }
                for node in self.pipeline
            ],
            "total_nodes": len(self.pipeline)
        }
