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
    # Check for direct DATABASE_URL (commonly provided by Cloud hosts like Render/Railway/Heroku)
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return db_url

    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "password")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432") or "5432"
    db_name = os.getenv("DB_NAME", "greek_tourism")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

def get_engine():
    """Returns a SQLAlchemy engine instance."""
    return create_engine(get_database_url())

def get_session():
    """Returns a new SQLAlchemy session."""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

# Create the engine eagerly so other modules can import it if needed
try:
    engine = get_engine()
except SystemExit:
    engine = None