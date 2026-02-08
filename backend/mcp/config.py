"""
Configuration for MCP server in the Todo AI Chatbot application.
"""
from typing import Optional
from pydantic import BaseSettings
import os


class MCPSettings(BaseSettings):
    """MCP server settings loaded from environment variables."""

    # MCP Server settings
    MCP_HOST: str = os.getenv("MCP_HOST", "localhost")
    MCP_PORT: int = int(os.getenv("MCP_PORT", "8001"))
    MCP_SERVER_NAME: str = os.getenv("MCP_SERVER_NAME", "todo-chatbot-mcp")

    # MCP Authentication (if needed)
    MCP_AUTH_TOKEN: Optional[str] = os.getenv("MCP_AUTH_TOKEN", None)

    # MCP Timeout settings
    MCP_REQUEST_TIMEOUT: int = int(os.getenv("MCP_REQUEST_TIMEOUT", "30"))
    MCP_CONNECTION_TIMEOUT: int = int(os.getenv("MCP_CONNECTION_TIMEOUT", "10"))

    # MCP Logging
    MCP_LOG_LEVEL: str = os.getenv("MCP_LOG_LEVEL", "INFO")
    MCP_ENABLE_LOGGING: bool = os.getenv("MCP_ENABLE_LOGGING", "true").lower() == "true"

    class Config:
        env_file = ".env"


# Global MCP settings instance
mcp_settings = MCPSettings()