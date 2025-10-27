from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    # API
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash-latest"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Memory
    vector_store_dim: int = 768
    max_context_length: int = 8000
    
    # MCP
    mcp_server_name: str = "agent-ia-mcp"
    mcp_version: str = "1.0.0"
    
    # RRLA Config
    max_reasoning_steps: int = 5
    confidence_threshold: float = 0.7
    
    # GitMCP
    gitmcp_enabled: bool = True

@lru_cache
def get_settings() -> Settings:
    return Settings()
