"""
Schema definitions for the chat API in the Todo AI Chatbot application.
"""
from pydantic import BaseModel, Field
from typing import Literal
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class UserMessage(BaseModel):
    """
    Schema for user message input.
    """
    role: Literal["user"] = Field(default="user", description="Role of the message sender")
    content: str = Field(..., min_length=1, max_length=10000, description="Content of the message")


class Metadata(BaseModel):
    """
    Schema for message metadata.
    """
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp of the message")
    client_info: Optional[Dict[str, Any]] = Field(default=None, description="Information about the client")


class ChatRequest(BaseModel):
    """
    Schema for the chat API request.
    """
    message: UserMessage = Field(..., description="User message to process")
    metadata: Optional[Metadata] = Field(default=None, description="Additional metadata for the request")


class ToolCall(BaseModel):
    """
    Schema for tool calls made by the agent.
    """
    id: str = Field(..., description="Unique identifier for the tool call")
    type: Literal["function"] = Field(default="function", description="Type of tool call")
    function: Dict[str, Any] = Field(..., description="Function details including name and arguments")


class ToolResult(BaseModel):
    """
    Schema for results from tool executions.
    """
    tool_call_id: str = Field(..., description="ID of the corresponding tool call")
    result: Dict[str, Any] = Field(..., description="Result from the tool execution")


class AssistantMessage(BaseModel):
    """
    Schema for assistant message response.
    """
    role: Literal["assistant"] = Field(default="assistant", description="Role of the message sender")
    content: str = Field(..., description="Content of the assistant's response")
    tool_calls: Optional[List[ToolCall]] = Field(default=None, description="List of tool calls made by the assistant")
    tool_results: Optional[List[ToolResult]] = Field(default=None, description="Results from tool executions")


class ResponseMetadata(BaseModel):
    """
    Schema for response metadata.
    """
    processing_time_ms: int = Field(..., description="Time taken to process the request in milliseconds")


class ChatResponse(BaseModel):
    """
    Schema for the chat API response.
    """
    conversation_id: str = Field(..., description="Unique identifier for the conversation")
    response: AssistantMessage = Field(..., description="Assistant's response to the user message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the response")
    metadata: Optional[ResponseMetadata] = Field(default=None, description="Additional response metadata")


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    success: bool = Field(default=False)
    error: str = Field(..., description="Error message")
    message: str = Field(..., description="Human-readable error message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the error")


class ConversationHistory(BaseModel):
    """
    Schema for conversation history.
    """
    conversation_id: str = Field(..., description="ID of the conversation")
    messages: List[Dict[str, Any]] = Field(..., description="List of messages in the conversation")
    created_at: datetime = Field(..., description="When the conversation was created")
    updated_at: datetime = Field(..., description="When the conversation was last updated")


class ListConversationsResponse(BaseModel):
    """
    Schema for listing conversations response.
    """
    conversations: List[ConversationHistory] = Field(..., description="List of user's conversations")
    total_count: int = Field(..., description="Total number of conversations")
    returned_count: int = Field(..., description="Number of conversations returned in this response")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the response")


class DeleteConversationResponse(BaseModel):
    """
    Schema for conversation deletion response.
    """
    success: bool = Field(default=True)
    conversation_id: str = Field(..., description="ID of the deleted conversation")
    message: str = Field(..., description="Confirmation message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the deletion")


class TaskData(BaseModel):
    """
    Schema for task-related data in responses.
    """
    id: str = Field(..., description="Unique identifier for the task")
    title: str = Field(..., description="Title of the task")
    description: Optional[str] = Field(default=None, description="Description of the task")
    due_date: Optional[datetime] = Field(default=None, description="Due date for the task")
    priority: str = Field(default="medium", description="Priority level of the task")
    category: Optional[str] = Field(default=None, description="Category of the task")
    completed: bool = Field(default=False, description="Completion status of the task")
    created_at: datetime = Field(..., description="When the task was created")
    updated_at: datetime = Field(..., description="When the task was last updated")


class TaskOperationResponse(BaseModel):
    """
    Schema for task operation responses.
    """
    success: bool
    task_id: Optional[str] = Field(default=None, description="ID of the affected task")
    message: str = Field(..., description="Result message")
    task: Optional[TaskData] = Field(default=None, description="Task data if relevant")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the response")


class HealthCheckResponse(BaseModel):
    """
    Schema for health check response.
    """
    status: str = Field(default="healthy", description="Health status of the service")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the check")
    version: str = Field(default="1.0.0", description="Version of the service")
    uptime: Optional[float] = Field(default=None, description="Uptime in seconds")