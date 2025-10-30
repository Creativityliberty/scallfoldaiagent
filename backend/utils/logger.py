import sys
from loguru import logger
from pathlib import Path

def setup_logger(log_level: str = "INFO", log_file: str | None = None) -> None:
    """
    Configure le logger global avec loguru.

    Args:
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR)
        log_file: Chemin vers le fichier de log (optionnel)
    """
    # Remove default handler
    logger.remove()

    # Console handler avec couleurs
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # File handler si spécifié
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
        )

    logger.info(f"Logger configured (level={log_level})")

def get_logger(name: str):
    """
    Retourne un logger avec un nom spécifique.

    Args:
        name: Nom du logger (généralement __name__)

    Returns:
        Logger configuré
    """
    return logger.bind(name=name)

# Setup par défaut
setup_logger()
