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
from .mcp import mcp_server

# Config
settings = get_settings()
app = FastAPI(
    title="Agent IA - Gemini + MCP + PocketFlow",
    version="1.0.0",
    description="Agent IA complet avec architecture RRLA et protocole MCP"
)

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
frontend_dir = root / "frontend"

if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
else:
    logger.warning(f"Frontend directory not found: {frontend_dir}")

# Services
orchestrator = Orchestrator()
gemini = GeminiClient(settings.gemini_api_key, settings.gemini_model)

# === ROUTES ===

@app.get("/")
def index():
    """Page d'accueil."""
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Agent IA Backend - Frontend not found"}

@app.post("/api/chat")
async def chat(req: Request):
    """
    Endpoint REST classique (non-streaming).
    Traite une requête utilisateur et retourne la réponse complète.
    """
    try:
        payload = await req.json()
        user_input = payload.get("input", "")

        if not user_input:
            raise HTTPException(400, "Missing 'input' field")

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
                "confidence": result.get("confidence", 0.0),
                "status": result.get("status", "unknown")
            }
        })

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(500, f"Internal error: {str(e)}")

@app.get("/api/stream")
async def stream_chat(prompt: str):
    """
    Endpoint SSE pour streaming token-par-token.
    Utilise Server-Sent Events pour envoyer les tokens en temps réel.
    """

    async def event_generator() -> AsyncGenerator[bytes, None]:
        try:
            # Stream depuis Gemini
            async for chunk in gemini.stream(prompt):
                # Format SSE
                yield f"data: {chunk}\n\n".encode("utf-8")

            # Fin du stream
            yield b"event: done\ndata: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"event: error\ndata: {str(e)}\n\n".encode("utf-8")

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
    """Informations sur le serveur MCP."""
    return JSONResponse(mcp_server.get_server_info())

@app.get("/api/mcp/tools")
def mcp_tools():
    """Liste des outils MCP disponibles."""
    return JSONResponse({
        "tools": mcp_server.list_tools(),
        "count": len(mcp_server.tools)
    })

@app.get("/api/mcp/tools/schema")
def mcp_tools_schema():
    """Schémas complets des outils MCP (pour Gemini function calling)."""
    return JSONResponse({
        "tools": mcp_server.get_tools_schema()
    })

@app.post("/api/mcp/call")
async def mcp_call(req: Request):
    """
    Appel d'un outil MCP.

    Body:
    {
        "tool": "search_memory",
        "arguments": {"query": "test", "top_k": 5}
    }
    """
    try:
        payload = await req.json()
        tool_name = payload.get("tool")
        arguments = payload.get("arguments", {})

        if not tool_name:
            raise HTTPException(400, "Missing 'tool' parameter")

        result = await mcp_server.call_tool(tool_name, arguments)
        # Sanitize error messages to avoid exposing internal details
        if isinstance(result, dict) and not result.get("success", True):
            # Log the full error internally but return a generic message
            logger.error(f"Tool {tool_name} failed: {result.get('error')}")
            return JSONResponse({"success": False, "error": "Tool execution failed"})
        return JSONResponse(result)

    except ValueError as e:
        # Only expose "Unknown tool" errors, sanitize others
        error_msg = str(e)
        if "Unknown tool" in error_msg:
            raise HTTPException(404, "Tool not found")
        else:
            logger.error(f"MCP validation error: {e}")
            raise HTTPException(400, "Invalid request")
    except Exception as e:
        logger.error(f"MCP call error: {e}")
        # Don't expose internal error details to external users
        raise HTTPException(500, "Tool execution error")

@app.get("/api/pipeline/info")
def pipeline_info():
    """Informations sur le pipeline d'orchestration."""
    return JSONResponse(orchestrator.get_pipeline_info())

@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model": settings.gemini_model,
        "mcp_tools": len(mcp_server.tools),
        "pipeline_nodes": len(orchestrator.pipeline)
    }

@app.get("/api/stats")
def stats():
    """Statistiques globales du système."""
    return {
        "orchestrator": orchestrator.get_pipeline_info(),
        "mcp": {
            "server_name": mcp_server.name,
            "version": mcp_server.version,
            "tools_count": len(mcp_server.tools)
        },
        "config": {
            "model": settings.gemini_model,
            "max_context": settings.max_context_length,
            "debug": settings.debug
        }
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Agent IA Backend starting...")
    logger.info(f"📦 Model: {settings.gemini_model}")
    logger.info(f"🔧 MCP Tools: {len(mcp_server.tools)}")
    logger.info(f"🧠 Pipeline Nodes: {len(orchestrator.pipeline)}")
    logger.info(f"🌐 Server: {settings.host}:{settings.port}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 Agent IA Backend shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info" if settings.debug else "warning"
    )
