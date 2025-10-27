from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import AsyncGenerator
import uuid
from loguru import logger

from .config import get_settings
from .core.orchestrator import Orchestrator
from .core.shared import Shared
from .llm.gemini_client import GeminiClient
from .mcp.server import mcp_server
from .integrations.gitmcp import GitMCPClient

# Config
settings = get_settings()
app = FastAPI(title="Agent IA - Gemini + MCP + PocketFlow", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
root = Path(__file__).resolve().parents[1]
front = root / "frontend"
app.mount("/static", StaticFiles(directory=front), name="static")

# Services
orchestrator = Orchestrator()
gemini = GeminiClient(settings.gemini_api_key, settings.gemini_model)

# === ROUTES ===

@app.get("/")
def index():
    return FileResponse(front / "index.html")

@app.post("/api/chat")
async def chat(req: Request):
    """Endpoint REST classique (non-streaming)."""
    payload = await req.json()
    user_input = payload.get("input", "")
    
    # Créer shared context
    shared = Shared()
    shared.set_metadata("flow_id", str(uuid.uuid4()))
    shared.set_metadata("user_id", payload.get("user_id", "anonymous"))
    shared.set_context("user_input", user_input)
    
    # Exécuter le flow
    result = await orchestrator.run(shared)
    
    return JSONResponse({
        "answer": result.get("answer", ""),
        "meta": {
            "flow_id": shared.get_metadata("flow_id"),
            "trace": [
                {
                    "node": t.node,
                    "status": t.status.value,
                    "duration_ms": t.duration_ms
                }
                for t in shared.get_trace()
            ],
            "confidence": result.get("confidence", 0.0)
        }
    })

@app.get("/api/stream")
async def stream_chat(prompt: str):
    """Endpoint SSE pour streaming token-par-token."""
    
    async def event_generator() -> AsyncGenerator[bytes, None]:
        try:
            # Préparation du prompt via orchestrator (optionnel)
            # Pour simplifier, on stream direct
            
            async for chunk in gemini.stream(prompt):
                # Format SSE
                yield f"data: {chunk}\n\n".encode("utf-8")
            
            # Fin du stream
            yield b"event: done\ndata: end\n\n"
            
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield b"event: error\ndata: internal_error\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        }
    )

@app.get("/api/mcp/info")
def mcp_info():
    """Info du serveur MCP."""
    return JSONResponse(mcp_server.get_server_info())

@app.get("/api/mcp/tools")
def mcp_tools():
    """Liste des outils MCP disponibles."""
    return JSONResponse({"tools": mcp_server.get_tools_schema()})

@app.post("/api/mcp/call")
async def mcp_call(req: Request):
    """Appel d'un outil MCP."""
    payload = await req.json()
    tool_name = payload.get("tool")
    arguments = payload.get("arguments", {})
    
    if not tool_name:
        raise HTTPException(400, "Missing 'tool' parameter")
    
    result = await mcp_server.call_tool(tool_name, arguments)
    return JSONResponse(result)

@app.post("/api/gitmcp/fetch")
async def fetch_gitmcp_context(req: Request):
    """Récupère le contexte d'un repo GitHub via GitMCP."""
    payload = await req.json()
    repo_url = payload.get("url", "")
    
    if not repo_url:
        raise HTTPException(400, "Missing 'url' parameter")
    
    context = await GitMCPClient.fetch_context(repo_url)
    return JSONResponse(context)

@app.get("/health")
def health():
    return {"status": "ok", "model": settings.gemini_model}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
