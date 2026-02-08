"""
MCP-specific data models for the Todo AI Chatbot application.
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime


class MCPToolCall(BaseModel):
    """
    Represents a tool call made during an MCP interaction.
    """
    id: str
    type: str
    function: Dict[str, Any]  # Contains name and arguments


class MCPToolResult(BaseModel):
    """
    Represents the result from an MCP tool execution.
    """
    tool_call_id: str
    result: Dict[str, Any]


class MCPTaskOperation(Enum):
    """
    Enumeration of possible task operations via MCP tools.
    """
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    UPDATE_TASK = "update_task"


class MCPTaskRequest(BaseModel):
    """
    Request model for task operations via MCP tools.
    """
    operation: MCPTaskOperation
    parameters: Dict[str, Any]
    user_context: Optional[Dict[str, Any]] = None  # Contains user_id and other context


class MCPTaskResponse(BaseModel):
    """
    Response model for task operations via MCP tools.
    """
    success: bool
    operation: MCPTaskOperation
    result: Dict[str, Any]
    error_message: Optional[str] = None
    timestamp: datetime = datetime.now()


class MCPConversationContext(BaseModel):
    """
    Context model for maintaining conversation state across MCP tool calls.
    """
    conversation_id: str
    user_id: str
    message_history: List[Dict[str, Any]]
    current_tool_calls: List[MCPToolCall]
    tool_results: List[MCPToolResult]
    last_updated: datetime = datetime.now()


class MCPAuthenticationContext(BaseModel):
    """
    Authentication context for MCP tool access.
    """
    user_id: str
    jwt_token: str
    permissions: List[str]
    expires_at: datetime