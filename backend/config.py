from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

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

    # Agents Configuration
    lead_gen_enabled: bool = True
    lead_gen_max_results: int = 50
    social_media_enabled: bool = True
    wordpress_enabled: bool = True
    wordpress_url: Optional[str] = None

    # External APIs
    google_places_api_key: Optional[str] = None
    dalle_api_key: Optional[str] = None
    unsplash_api_key: Optional[str] = None

    # Content & SEO
    default_tone: str = "professional"
    target_word_count: int = 1800
    enable_yoast: bool = True
    min_seo_score: int = 70

    # Media
    use_dalle: bool = True
    images_per_article: int = 4
    optimize_images: bool = True

    # Batch Processing
    batch_max_concurrent: int = 3
    batch_retry_on_failure: bool = True

    # Output Directories
    output_dir_leads: str = "./output_leads"
    output_dir_social: str = "./output_social_media"
    output_dir_blog: str = "./output_blog_articles"

@lru_cache
def get_settings() -> Settings:
    return Settings()
