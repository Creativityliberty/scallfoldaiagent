from loguru import logger
import os

# Configuration simple; peut être étendue (JSON, context vars, etc.)
level = "DEBUG" if os.getenv("DEBUG", "false").lower() == "true" else "INFO"
logger.remove()
logger.add(lambda msg: print(msg, end=""), level=level)
