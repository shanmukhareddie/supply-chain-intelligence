"""
logger.py
─────────
Centralised logging setup using loguru.
Import `logger` from here instead of configuring it per-module.

Usage:
    from logger import logger
    logger.info("Pipeline started")
    logger.error("Something went wrong: {err}", err=e)
"""

import sys
from config import config
from loguru import logger

# Remove default handler
logger.remove()

# Console handler — colourised, human-readable
logger.add(
    sys.stdout,
    level=config.log_level,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
    colorize=True,
)

# File handler — full detail, rotates daily
logger.add(
    "logs/pipeline_{time:YYYY-MM-DD}.log",
    level="DEBUG",
    rotation="1 day",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
)

# Re-export for clean imports
__all__ = ["logger"]
