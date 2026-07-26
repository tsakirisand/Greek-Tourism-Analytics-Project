"""
Database connection and session management module with Streamlit resource caching.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from logger import logger

load_dotenv()


def get_database_url() -> str:
    """Constructs the PostgreSQL or SQLite database URL from environment variables.

    Returns:
        str: Fully qualified database connection string URL.
    """
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        if "@" in db_url:
            base, target = db_url.rsplit("@", 1)
            target = target.replace(":/", "/")
            db_url = f"{base}@{target}"
        return db_url

    user = os.getenv("DB_USER", "postgres") or "postgres"
    password = os.getenv("DB_PASSWORD", "password") or "password"
    host = os.getenv("DB_HOST", "localhost") or "localhost"

    port_env = str(os.getenv("DB_PORT", "")).strip()
    port = port_env if (port_env and port_env.isdigit()) else "5432"

    db_name = os.getenv("DB_NAME", "greek_tourism") or "greek_tourism"

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def _create_engine_instance() -> Optional[Engine]:
    """Helper to create SQLAlchemy engine with pooling configuration.

    Returns:
        Optional[Engine]: SQLAlchemy engine instance or None on error.
    """
    try:
        url = get_database_url()
        # Enable connection pooling options for production PostgreSQL
        if "sqlite" in url:
            engine_inst = create_engine(url)
        else:
            engine_inst = create_engine(
                url, pool_pre_ping=True, pool_size=10, max_overflow=20
            )
        logger.info("Database engine created successfully.")
        return engine_inst
    except Exception as e:
        logger.error(f"Could not create database engine: {e}")
        return None


def get_engine() -> Optional[Engine]:
    """Returns SQLAlchemy engine instance, cached with st.cache_resource if Streamlit active.

    Returns:
        Optional[Engine]: Cached or new engine instance.
    """
    try:
        import streamlit as st

        @st.cache_resource
        def _cached_engine():
            return _create_engine_instance()

        return _cached_engine()
    except (ImportError, Exception):
        # Fallback if Streamlit context is not available or during pytest
        return _create_engine_instance()


def get_session() -> Optional[Session]:
    """Returns a new SQLAlchemy ORM session bound to the active engine.

    Returns:
        Optional[Session]: New SQLAlchemy Session instance or None.
    """
    engine_inst = get_engine()
    if not engine_inst:
        logger.error("Cannot create session: Engine is unavailable.")
        return None
    session_factory = sessionmaker(bind=engine_inst)
    return session_factory()


# Global engine instance for legacy direct imports
try:
    engine = get_engine()
except Exception:
    engine = None
