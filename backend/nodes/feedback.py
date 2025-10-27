from ..core.base_node import BaseNode
from typing import Any, Dict

class FeedbackNode(BaseNode):
    def __init__(self):
        super().__init__("feedback")
    
    async def exec(self, input_data: Any) -> Dict[str, Any]:
        # Placeholder pour collecte de feedback utilisateur
        return {"ack": True}
