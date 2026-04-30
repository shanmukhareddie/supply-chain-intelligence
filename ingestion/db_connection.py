"""
db_connection.py
────────────────
Single source of truth for database connections.
Reads credentials from .env — never hardcode them.

Usage:
    from ingestion.db_connection import get_engine, get_session

    engine = get_engine()
    with get_session() as session:
        session.execute(...)
"""

import os
from contextlib import contextmanager

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()


def _build_connection_url() -> str:
    """Build the PostgreSQL connection URL from environment variables."""
    # Allow a full DATABASE_URL override (Supabase provides this)
    if url := os.getenv("DATABASE_URL"):
        return url

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "supply_chain")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


def get_engine():
    """
    Create and return a SQLAlchemy engine.
    Connection pooling is handled automatically.
    """
    url = _build_connection_url()
    engine = create_engine(
        url,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,   # check connection health before use
        echo=False,           # set True to log all SQL (useful for debugging)
    )
    return engine


def get_session_factory(engine=None):
    """Return a session factory bound to the engine."""
    if engine is None:
        engine = get_engine()
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextmanager
def get_session(engine=None) -> Session:
    """
    Context manager for database sessions.
    Automatically commits on success, rolls back on error.

    Example:
        with get_session() as session:
            session.execute(text("SELECT 1"))
    """
    SessionLocal = get_session_factory(engine)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def test_connection() -> bool:
    """
    Quick health check — call this at pipeline startup.
    Returns True if connection is successful.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


if __name__ == "__main__":
    # Run this file directly to test your connection:
    # python -m ingestion.db_connection
    ok = test_connection()
    if ok:
        print("Connected successfully!")
    else:
        print("Connection failed. Check your .env file.")
