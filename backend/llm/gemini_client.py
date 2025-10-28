import os
from typing import AsyncGenerator, Dict, Any, List
from google import genai
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

class GeminiClient:
    """Client Gemini avec support streaming et retry logic."""

    def __init__(self, api_key: str | None = None, model: str = "gemini-1.5-flash-latest"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.client = genai.Client(api_key=self.api_key)
        logger.info(f"GeminiClient initialized with model: {model}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Génération simple (non-streaming)."""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=genai.GenerateContentConfig(**kwargs)
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            raise

    async def stream(self, prompt: str, **kwargs: Any) -> AsyncGenerator[str, None]:
        """Génération streaming token par token."""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=genai.GenerateContentConfig(
                    **kwargs,
                    response_modalities=["TEXT"]
                ),
                stream=True
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Gemini streaming error: {e}")
            yield f"[ERROR: {str(e)}]"

    async def generate_with_tools(
        self,
        prompt: str,
        tools: List[Dict[str, Any]],
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Génération avec function calling (pour MCP)."""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=genai.GenerateContentConfig(
                    tools=tools,
                    **kwargs
                )
            )

            return {
                "text": response.text if response.text else None,
                "function_calls": response.candidates[0].content.parts
                if response.candidates
                else []
            }
        except Exception as e:
            logger.error(f"Gemini tools error: {e}")
            raise
