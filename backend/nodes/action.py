from ..core.base_node import BaseNode
from ..core.shared import Shared
from typing import Dict, Any

class ActionNode(BaseNode):
    def __init__(self):
        super().__init__("action")
    
    def prep(self, shared: Shared) -> Dict[str, Any]:
        return {"synthesis": shared.get_result("synthesis")}
    
    async def exec(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        synthesis = input_data["synthesis"] or {"draft": ""}
        
        return {
            "final": synthesis["draft"],
            "format": "text",
            "actions_taken": [],
            "status": "completed"
        }
