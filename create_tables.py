"""
Script to create the database schema.
"""
from database import get_engine
from models import Base

def init_db():
    """Creates all tables defined in models."""
    print("Initializing database schema...")
    engine = get_engine()
    
    # Create all tables
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_db()