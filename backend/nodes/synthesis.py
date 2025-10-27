from ..core.base_node import BaseNode
from ..core.shared import Shared
from typing import Dict, Any

class SynthesisNode(BaseNode):
    def __init__(self):
        super().__init__("synthesis")
    
    def prep(self, shared: Shared) -> Dict[str, Any]:
        return {
            "reasoning": shared.get_result("reasoning"),
            "input": shared.get_result("perception", "clean_input")
        }
    
    async def exec(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        reasoning = input_data["reasoning"] or {}
        draft = f"Synthèse basée sur {len(reasoning.get('steps', []))} étapes de raisonnement."
        
        return {
            "draft": draft,
            "sources": [],
            "confidence": reasoning.get("confidence", 0.5)
        }
