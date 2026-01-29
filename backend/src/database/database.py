from sqlmodel import create_engine, Session
from typing import Generator
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/todo_app")

# Create engine with appropriate settings for Neon PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_size=10,     # Increase pool size for concurrent requests
    max_overflow=20,  # Allow additional connections when needed
    connect_args={
        "sslmode": "require",  # Require SSL for Neon
        "connect_timeout": 10, # Set connection timeout to 10 seconds
    }
)

def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection in FastAPI.
    """
    with Session(engine) as session:
        yield session


