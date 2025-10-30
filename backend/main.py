from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import AsyncGenerator
from contextlib import asynccontextmanager
import uuid
from loguru import logger

from .config import get_settings
from .core.orchestrator import Orchestrator
from .core.shared import Shared
from .llm.gemini_client import GeminiClient
from .mcp import mcp_server
from .agents import LeadGeneratorAgent, SocialMediaManagerAgent, WordPressBloggerAgent

# Config
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info("🚀 Agent IA Backend starting...")
    logger.info(f"📦 Model: {settings.gemini_model}")
    logger.info(f"🔧 MCP Tools: {len(mcp_server.tools)}")
    
    # Initialize agents
    app.state.agents = {}
    
    if settings.lead_gen_enabled:
        app.state.agents["lead_generator"] = LeadGeneratorAgent(
            orchestrator=orchestrator,
            mcp_server=mcp_server,
            max_results=settings.lead_gen_max_results
        )
        logger.info("✓ Lead Generator Agent initialized")
    
    if settings.social_media_enabled:
        app.state.agents["social_media"] = SocialMediaManagerAgent(
            orchestrator=orchestrator,
            mcp_server=mcp_server,
            default_tone=settings.default_tone
        )
        logger.info("✓ Social Media Manager Agent initialized")
    
    if settings.wordpress_enabled:
        app.state.agents["wordpress"] = WordPressBloggerAgent(
            orchestrator=orchestrator,
            mcp_server=mcp_server,
            wordpress_url=settings.wordpress_url,
            target_word_count=settings.target_word_count,
            min_seo_score=settings.min_seo_score
        )
        logger.info("✓ WordPress Blogger Agent initialized")
    
    logger.info(f"🤖 {len(app.state.agents)} agents initialized")
    logger.info(f"🌐 Server: {settings.host}:{settings.port}")
    
    yield
    
    # Shutdown
    logger.info("👋 Agent IA Backend shutting down...")

app = FastAPI(
    title="Agent IA - Gemini + MCP + PocketFlow",
    version="2.0.0",
    description="Agent IA complet avec architecture RRLA, protocole MCP et agents spécialisés",
    lifespan=lifespan
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

@app.get("/api/agents")
def list_agents():
    """List all available agents."""
    agents_info = []
    for name, agent in app.state.agents.items():
        agents_info.append(agent.get_info())
    
    return JSONResponse({
        "agents": agents_info,
        "count": len(agents_info)
    })

@app.post("/api/agents/{agent_name}/execute")
async def execute_agent(agent_name: str, request: Request):
    """
    Execute a specific agent with task parameters.
    
    Args:
        agent_name: Name of the agent (lead_generator, social_media, wordpress)
        
    Body:
        Task-specific parameters
    """
    try:
        if agent_name not in app.state.agents:
            raise HTTPException(404, f"Agent '{agent_name}' not found")
        
        payload = await request.json()
        agent = app.state.agents[agent_name]
        
        logger.info(f"Executing agent: {agent_name}")
        result = await agent.execute(payload)
        
        return JSONResponse(result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent execution error: {e}", exc_info=True)
        raise HTTPException(500, f"Agent execution failed: {str(e)}")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Agent management dashboard."""
    dashboard_path = frontend_dir / "agent-dashboard.html"
    if dashboard_path.exists():
        return FileResponse(dashboard_path)
    return HTMLResponse("""
        <html>
            <head><title>Agent Dashboard</title></head>
            <body>
                <h1>Agent Dashboard</h1>
                <p>Dashboard interface is being developed.</p>
                <p><a href="/">Back to main interface</a></p>
            </body>
        </html>
    """)

@app.get("/wordpress", response_class=HTMLResponse)
async def wordpress_ui():
    """WordPress management interface."""
    wordpress_path = frontend_dir / "wordpress-dashboard.html"
    if wordpress_path.exists():
        return FileResponse(wordpress_path)
    return HTMLResponse("""
        <html>
            <head><title>WordPress Dashboard</title></head>
            <body>
                <h1>WordPress Dashboard</h1>
                <p>WordPress interface is being developed.</p>
                <p><a href="/">Back to main interface</a></p>
            </body>
        </html>
    """)

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
    agents_stats = {}
    for name, agent in app.state.agents.items():
        agents_stats[name] = {
            "description": agent.description,
            "tools": agent.tools
        }
    
    return {
        "version": "2.0.0",
        "orchestrator": orchestrator.get_pipeline_info(),
        "agents": {
            "enabled": list(app.state.agents.keys()),
            "count": len(app.state.agents),
            "details": agents_stats
        },
        "mcp": {
            "server_name": mcp_server.name,
            "version": mcp_server.version,
            "tools_count": len(mcp_server.tools)
        },
        "config": {
            "model": settings.gemini_model,
            "max_context": settings.max_context_length,
            "debug": settings.debug,
            "wordpress_enabled": settings.wordpress_enabled,
            "lead_gen_enabled": settings.lead_gen_enabled,
            "social_media_enabled": settings.social_media_enabled
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info" if settings.debug else "warning"
    )
