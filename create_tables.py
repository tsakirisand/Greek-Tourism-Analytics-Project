"""
Script to create the database schema and indexes.
"""

from database import get_engine
from logger import logger
from models import Base


def init_db() -> None:
    """Creates all tables and indexes defined in SQLAlchemy models."""
    logger.info("Initializing database schema and indexes...")
    engine = get_engine()
    if engine is None:
        logger.error("Database engine could not be initialized.")
        return

    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables and indexes created successfully!")
    except Exception as e:
        logger.error(f"Error creating database schema: {e}")
        raise


if __name__ == "__main__":
    init_db()
