"""
Message model for the Todo AI Chatbot application.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
import enum


class MessageRoleEnum(str, enum.Enum):
    user = "user"
    assistant = "assistant"


class ToolCall(SQLModel):
    id: str
    type: str
    function: Dict[str, Any]


class ToolResult(SQLModel):
    tool_call_id: str
    result: Dict[str, Any]


class MessageBase(SQLModel):
    role: MessageRoleEnum
    content: str = Field(nullable=False)
    tool_calls: Optional[List[ToolCall]] = Field(default=None)
    tool_results: Optional[List[ToolResult]] = Field(default=None)


class Message(MessageBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id", nullable=False)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship - assuming Conversation and User models exist elsewhere
    # conversation: "Conversation" = Relationship(back_populates="messages")


class MessageRead(MessageBase):
    id: UUID
    created_at: datetime


class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_results: Optional[List[ToolResult]] = None