"""
tests/test_connection.py
────────────────────────
Day 1 smoke tests — verify the project structure and config are correct.
These tests do NOT require a real database connection.
"""

import os
import pytest


def test_env_example_exists():
    """The .env.example file must be present and committed."""
    assert os.path.exists(".env.example"), (
        ".env.example is missing — create it so teammates know what vars to set"
    )


def test_required_env_vars_documented():
    """All critical env vars must appear in .env.example."""
    with open(".env.example") as f:
        content = f.read()
    required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    for var in required:
        assert var in content, f"{var} is not documented in .env.example"


def test_project_structure():
    """All required folders and __init__.py files must exist."""
    required_paths = [
        "ingestion/__init__.py",
        "ingestion/sources/__init__.py",
        "ingestion/transform/__init__.py",
        "ingestion/load/__init__.py",
        "tests/__init__.py",
        "requirements.txt",
        ".gitignore",
        "config.py",
    ]
    for path in required_paths:
        assert os.path.exists(path), f"Missing required file: {path}"


def test_gitignore_excludes_env():
    """.gitignore must exclude .env to prevent secret leaks."""
    with open(".gitignore") as f:
        content = f.read()
    assert ".env" in content, ".gitignore must contain .env"


def test_config_loads():
    """Config dataclass must load without errors."""
    from config import config
    assert config.batch_size > 0
    assert config.data_start_year == "2015"
    assert len(config.commodity_codes) > 0


def test_requirements_has_core_libs():
    """requirements.txt must include all core dependencies."""
    with open("requirements.txt") as f:
        content = f.read()
    core = ["pandas", "sqlalchemy", "psycopg2", "python-dotenv", "requests", "pytest"]
    for lib in core:
        assert lib in content, f"{lib} is missing from requirements.txt"
