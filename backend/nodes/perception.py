from ..core.base_node import BaseNode
from ..core.shared import Shared
from typing import Dict, Any

class PerceptionNode(BaseNode):
    def __init__(self):
        super().__init__("perception")
    
    async def exec(self, input_data: Any) -> Dict[str, Any]:
        raw_input = input_data or ""
        clean_input = raw_input.strip()
        return {"clean_input": clean_input, "raw": raw_input}
