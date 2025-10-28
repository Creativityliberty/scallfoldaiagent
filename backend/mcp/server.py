from typing import Any, Dict, List, Callable, Awaitable
from dataclasses import dataclass
import json
from loguru import logger

@dataclass
class MCPTool:
    """Définition d'un outil MCP."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Callable[..., Awaitable[Any]]

class MCPServer:
    """
    Implémentation MCP (Model Context Protocol).
    Expose des outils que l'agent peut appeler via function calling.
    """

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.tools: Dict[str, MCPTool] = {}
        logger.info(f"MCP Server initialized: {name} v{version}")

    def register_tool(self, tool: MCPTool) -> None:
        """Enregistre un nouvel outil."""
        self.tools[tool.name] = tool
        logger.info(f"MCP tool registered: {tool.name}")

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Retourne les schémas pour Gemini function calling."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema
            }
            for tool in self.tools.values()
        ]

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Exécute un outil MCP."""
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")

        tool = self.tools[name]
        logger.info(f"Calling MCP tool: {name} with args: {arguments}")

        try:
            result = await tool.handler(**arguments)
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"MCP tool error ({name}): {e}")
            return {"success": False, "error": str(e)}

    def get_server_info(self) -> Dict[str, Any]:
        """Info du serveur MCP."""
        return {
            "name": self.name,
            "version": self.version,
            "protocol_version": "1.0",
            "capabilities": {
                "tools": list(self.tools.keys()),
                "prompts": [],
                "resources": []
            }
        }

    def list_tools(self) -> List[Dict[str, str]]:
        """Liste tous les outils disponibles."""
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools.values()
        ]
