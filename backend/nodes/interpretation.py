from ..core.base_node import BaseNode
from typing import Dict, Any

class InterpretationNode(BaseNode):
    def __init__(self):
        super().__init__("interpretation")
    
    async def exec(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        text = input_data.get("clean_input", "")
        intent = "question" if "?" in text else "instruction"
        task_type = "qa" if intent == "question" else "generation"
        
        return {
            "intent": intent,
            "task_type": task_type,
            "entities": [],
            "sentiment": "neutral"
        }
