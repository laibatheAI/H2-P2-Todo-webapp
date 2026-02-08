"""
Database session management for the Todo AI Chatbot application.
"""
from sqlmodel import create_engine, Session
from sqlalchemy.pool import QueuePool
from backend.config import settings
from typing import Generator


# Create the database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO_LOG,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session from the sessionmaker.
    """
    with Session(engine) as session:
        yield session