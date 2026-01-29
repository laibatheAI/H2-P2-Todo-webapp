from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: str = Field(min_length=2, max_length=100)
    avatar: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    """
    User model representing a registered user with authentication credentials
    and basic profile information (name, email, avatar).
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str = Field(nullable=False)  # Hashed password
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Add any additional user-related methods here