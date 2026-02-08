"""
Conversation model for the Todo AI Chatbot application.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4


class ConversationBase(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)


class Conversation(ConversationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    last_accessed_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship - assuming User model exists elsewhere
    # user: "User" = Relationship(back_populates="conversations")
    # messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationRead(ConversationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_accessed_at: datetime


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(SQLModel):
    title: Optional[str] = None