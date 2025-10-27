from typing import List, Dict, Any

class ContextManager:
    def __init__(self, max_length: int = 8000):
        self.max_length = max_length
        self.history: List[Dict[str, Any]] = []
    
    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
    
    def snapshot(self) -> List[Dict[str, Any]]:
        return self.history[-10:]
