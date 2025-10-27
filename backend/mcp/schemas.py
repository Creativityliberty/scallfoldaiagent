from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class MCPToolCall(BaseModel):
    tool: str = Field(..., description="Nom de l'outil MCP à appeler")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments de l'outil")

class MCPToolResult(BaseModel):
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
