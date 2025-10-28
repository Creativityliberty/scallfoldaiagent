from .server import MCPServer, MCPTool
from .tools import (
    search_memory,
    store_memory,
    analyze_sentiment,
    extract_keywords,
    calculate,
    get_current_context
)
from .schemas import TOOL_SCHEMAS

# Instanciation globale du serveur MCP
mcp_server = MCPServer(
    name="agent-ia-mcp",
    version="1.0.0"
)

# Enregistrement de tous les outils
mcp_server.register_tool(MCPTool(
    name="search_memory",
    description="Recherche sémantique dans la mémoire de l'agent",
    input_schema=TOOL_SCHEMAS["search_memory"],
    handler=search_memory
))

mcp_server.register_tool(MCPTool(
    name="store_memory",
    description="Stocke un élément en mémoire pour référence future",
    input_schema=TOOL_SCHEMAS["store_memory"],
    handler=store_memory
))

mcp_server.register_tool(MCPTool(
    name="analyze_sentiment",
    description="Analyse le sentiment d'un texte (positif, négatif, neutre)",
    input_schema=TOOL_SCHEMAS["analyze_sentiment"],
    handler=analyze_sentiment
))

mcp_server.register_tool(MCPTool(
    name="extract_keywords",
    description="Extrait les mots-clés importants d'un texte",
    input_schema=TOOL_SCHEMAS["extract_keywords"],
    handler=extract_keywords
))

mcp_server.register_tool(MCPTool(
    name="calculate",
    description="Évalue une expression mathématique",
    input_schema=TOOL_SCHEMAS["calculate"],
    handler=calculate
))

mcp_server.register_tool(MCPTool(
    name="get_current_context",
    description="Récupère le contexte actuel de l'agent",
    input_schema=TOOL_SCHEMAS["get_current_context"],
    handler=get_current_context
))

__all__ = ["mcp_server", "MCPServer", "MCPTool"]
