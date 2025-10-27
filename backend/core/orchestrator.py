from typing import Dict, Any
from loguru import logger

from .shared import Shared
from ..nodes.perception import PerceptionNode
from ..nodes.interpretation import InterpretationNode
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
            ReasoningNode(),
            SynthesisNode(),
            ActionNode(),
        ]
        logger.info(f"Orchestrator initialized with {len(self.pipeline)} nodes")
    
    async def run(self, shared: Shared) -> Dict[str, Any]:
        """Exécute le flow complet."""
        logger.info(f"Starting flow {shared.get_metadata('flow_id')}")
        
        input_data = shared.get_context("user_input", None)
        
        for node in self.pipeline:
            try:
                logger.debug(f"Executing node: {node.name}")
                result, next_route = await node.run(shared, input_data)
                input_data = result
                
                # Gestion du routage conditionnel (si implémenté)
                if next_route:
                    logger.info(f"Routing to: {next_route}")
                    # Logique de routage personnalisée
                
            except Exception as e:
                logger.error(f"Node {node.name} failed: {e}")
                # Stratégie de fallback
                shared.set_result(node.name, {"error": str(e)})
                break
        
        # Résultat final
        final_result = shared.get_result("action")
        
        return {
            "answer": final_result.get("final") if final_result else "Erreur de traitement",
            "confidence": shared.get_result("reasoning", "confidence") or 0.0,
            "metadata": shared["metadata"],
            "trace": shared.get_trace()
        }
