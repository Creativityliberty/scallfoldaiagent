from .server import MCPServer, MCPTool
from .tools import (
    search_memory,
    store_memory,
    analyze_sentiment,
    extract_keywords,
    calculate,
    get_current_context
)
from .artifacts import (
    create_artifact,
    save_artifact,
    list_artifacts,
    update_artifact,
    delete_artifact
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
    description="Recherche s�mantique dans la m�moire de l'agent",
    input_schema=TOOL_SCHEMAS["search_memory"],
    handler=search_memory
))

mcp_server.register_tool(MCPTool(
    name="store_memory",
    description="Stocke un �l�ment en m�moire pour r�f�rence future",
    input_schema=TOOL_SCHEMAS["store_memory"],
    handler=store_memory
))

mcp_server.register_tool(MCPTool(
    name="analyze_sentiment",
    description="Analyse le sentiment d'un texte (positif, n�gatif, neutre)",
    input_schema=TOOL_SCHEMAS["analyze_sentiment"],
    handler=analyze_sentiment
))

mcp_server.register_tool(MCPTool(
    name="extract_keywords",
    description="Extrait les mots-cl�s importants d'un texte",
    input_schema=TOOL_SCHEMAS["extract_keywords"],
    handler=extract_keywords
))

mcp_server.register_tool(MCPTool(
    name="calculate",
    description="�value une expression math�matique",
    input_schema=TOOL_SCHEMAS["calculate"],
    handler=calculate
))

mcp_server.register_tool(MCPTool(
    name="get_current_context",
    description="R�cup�re le contexte actuel de l'agent",
    input_schema=TOOL_SCHEMAS["get_current_context"],
    handler=get_current_context
))

# === ARTIFACT TOOLS ===

mcp_server.register_tool(MCPTool(
    name="create_artifact",
    description="Crée un artifact (code, document, config, data)",
    input_schema=TOOL_SCHEMAS["create_artifact"],
    handler=create_artifact
))

mcp_server.register_tool(MCPTool(
    name="save_artifact",
    description="Sauvegarde un artifact sur le disque",
    input_schema=TOOL_SCHEMAS["save_artifact"],
    handler=save_artifact
))

mcp_server.register_tool(MCPTool(
    name="list_artifacts",
    description="Liste les artifacts créés",
    input_schema=TOOL_SCHEMAS["list_artifacts"],
    handler=list_artifacts
))

mcp_server.register_tool(MCPTool(
    name="update_artifact",
    description="Met à jour un artifact existant",
    input_schema=TOOL_SCHEMAS["update_artifact"],
    handler=update_artifact
))

mcp_server.register_tool(MCPTool(
    name="delete_artifact",
    description="Supprime un artifact",
    input_schema=TOOL_SCHEMAS["delete_artifact"],
    handler=delete_artifact
))

__all__ = ["mcp_server", "MCPServer", "MCPTool"]
