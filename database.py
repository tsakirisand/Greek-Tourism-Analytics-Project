"""
Database connection and session management.
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

def get_database_url() -> str:
    """Constructs the database URL from environment variables."""
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

def get_engine():
    """Returns a SQLAlchemy engine instance safely."""
    try:
        url = get_database_url()
        return create_engine(url)
    except Exception as e:
        print(f"Warning: Could not create database engine: {e}")
        return None

def get_session():
    """Returns a new SQLAlchemy session."""
    engine = get_engine()
    if not engine:
        return None
    Session = sessionmaker(bind=engine)
    return Session()

# Create the engine safely so other modules importing it will not crash
try:
    engine = get_engine()
except Exception:
    engine = None