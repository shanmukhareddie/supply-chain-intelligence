"""
config.py
─────────
Central configuration for the pipeline.
Import this anywhere instead of scattering os.getenv() calls.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class PipelineConfig:
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # Ingestion behaviour
    batch_size: int = int(os.getenv("PIPELINE_BATCH_SIZE", "1000"))

    # World Bank API
    world_bank_base_url: str = "http://api.worldbank.org/v2"
    world_bank_per_page: int = 500

    # Date range for historical ingestion
    data_start_year: str = "2015"
    data_end_year: str = "2024"

    # Commodity codes to track (World Bank indicator codes)
    commodity_codes: tuple = (
        "PCOALAU",   # Coal, Australian
        "POILAPSP",  # Crude oil, Brent
        "PNGAS",     # Natural gas
        "PWHEAMT",   # Wheat
        "PMAIZMT",   # Maize
    )


# Singleton — import this everywhere
config = PipelineConfig()
