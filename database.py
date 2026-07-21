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
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    # Error handling for missing env vars
    missing_vars = []
    if not user: missing_vars.append("DB_USER")
    if not password: missing_vars.append("DB_PASSWORD")
    if not host: missing_vars.append("DB_HOST")
    if not port: missing_vars.append("DB_PORT")
    if not db_name: missing_vars.append("DB_NAME")

    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please ensure your .env file is properly configured.")
        sys.exit(1)

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