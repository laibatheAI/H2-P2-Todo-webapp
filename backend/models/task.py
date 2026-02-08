"""
Task model for the Todo AI Chatbot application.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
import enum


class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    category: Optional[str] = Field(default=None, max_length=100)


class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    completed: bool = Field(default=False)
    completed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship - assuming User model exists elsewhere
    # user: "User" = Relationship(back_populates="tasks")


class TaskRead(TaskBase):
    id: UUID
    completed: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    category: Optional[str] = None
    completed: Optional[bool] = None