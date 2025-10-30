import pytest
from backend.mcp import mcp_server
from backend.mcp.tools import search_memory, calculate, analyze_sentiment

@pytest.mark.asyncio
async def test_mcp_server_initialization():
    """Test l'initialisation du serveur MCP."""
    assert mcp_server is not None
    assert mcp_server.name == "agent-ia-mcp"
    assert len(mcp_server.tools) > 0

def test_mcp_tools_registration():
    """Test l'enregistrement des outils."""
    tools = mcp_server.list_tools()

    assert len(tools) > 0
    assert any(tool["name"] == "search_memory" for tool in tools)
    assert any(tool["name"] == "calculate" for tool in tools)
    assert any(tool["name"] == "analyze_sentiment" for tool in tools)

def test_mcp_server_info():
    """Test les infos du serveur."""
    info = mcp_server.get_server_info()

    assert "name" in info
    assert "version" in info
    assert "capabilities" in info
    assert "tools" in info["capabilities"]

@pytest.mark.asyncio
async def test_search_memory_tool():
    """Test l'outil de recherche mémoire."""
    result = await search_memory(query="test", top_k=3)

    assert isinstance(result, list)
    assert len(result) <= 3
    assert all("content" in item for item in result)
    assert all("score" in item for item in result)

@pytest.mark.asyncio
async def test_calculate_tool():
    """Test l'outil de calcul."""
    result = await calculate("2 + 2")

    assert result["success"] is True
    assert result["result"] == 4.0

@pytest.mark.asyncio
async def test_calculate_tool_invalid():
    """Test l'outil de calcul avec une expression invalide."""
    result = await calculate("invalid expression")

    assert result["success"] is False
    assert "error" in result

@pytest.mark.asyncio
async def test_analyze_sentiment_tool():
    """Test l'outil d'analyse de sentiment."""
    result = await analyze_sentiment("C'est super génial !")

    assert "sentiment" in result
    assert "score" in result
    assert result["sentiment"] in ["positive", "negative", "neutral"]

@pytest.mark.asyncio
async def test_mcp_call_tool():
    """Test l'appel d'un outil via le serveur."""
    result = await mcp_server.call_tool("calculate", {"expression": "10 * 5"})

    assert result["success"] is True
    assert result["result"]["result"] == 50.0

@pytest.mark.asyncio
async def test_mcp_call_unknown_tool():
    """Test l'appel d'un outil inexistant."""
    with pytest.raises(ValueError):
        await mcp_server.call_tool("nonexistent_tool", {})

def test_mcp_tools_schema():
    """Test la récupération des schémas d'outils."""
    schemas = mcp_server.get_tools_schema()

    assert isinstance(schemas, list)
    assert len(schemas) > 0
    assert all("name" in schema for schema in schemas)
    assert all("description" in schema for schema in schemas)
    assert all("parameters" in schema for schema in schemas)
