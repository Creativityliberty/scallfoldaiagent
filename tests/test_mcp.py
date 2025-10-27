import asyncio
import pytest

from backend.mcp.server import mcp_server

@pytest.mark.asyncio
async def test_mcp_server_info_and_tool():
    info = mcp_server.get_server_info()
    assert info["name"] == "agent-ia-mcp"
    assert "search_memory" in info["capabilities"]["tools"]

    res = await mcp_server.call_tool("search_memory", {"query": "python", "top_k": 3})
    assert res["success"] is True
    assert isinstance(res["result"], list)
    assert len(res["result"]) == 3
