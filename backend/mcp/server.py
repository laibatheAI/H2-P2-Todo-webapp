"""
MCP server implementation for the Todo AI Chatbot application.
"""
from mcp.server import Server
from mcp.types import Notification, Result, Request
import asyncio
import logging
from typing import Dict, Any, List

from backend.mcp.tools.task_tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool,
)

# Initialize the MCP server
server = Server("todo-chatbot-mcp")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@server.after_shutdown
async def cleanup():
    """Cleanup function to run after the server shuts down."""
    logger.info("MCP Server shutting down...")


def register_tools():
    """Register all MCP tools with the server."""
    # Register the five required task management tools
    server.register_tool(add_task_tool)
    server.register_tool(list_tasks_tool)
    server.register_tool(complete_task_tool)
    server.register_tool(delete_task_tool)
    server.register_tool(update_task_tool)

    logger.info("All MCP tools registered successfully")


# Register tools when the server module is loaded
register_tools()


async def run_server(host: str = "localhost", port: int = 8001):
    """Run the MCP server."""
    logger.info(f"Starting MCP Server on {host}:{port}")
    async with server.serve_socket_strict(host, port):
        logger.info("MCP Server running...")
        # Keep the server running
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    # Run the server if this file is executed directly
    asyncio.run(run_server())