"""
Configuration module for Todo AI Chatbot application.
"""
from typing import Optional
from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")
    DB_ECHO_LOG: bool = os.getenv("DB_ECHO_LOG", "false").lower() == "true"

    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # MCP Server settings
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8001"))

    # Application settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))

    # Conversation settings
    MAX_MESSAGE_HISTORY: int = int(os.getenv("MAX_MESSAGE_HISTORY", "50"))

    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()