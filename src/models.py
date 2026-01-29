from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with ID, title, description, completion status, and creation timestamp.

    Attributes:
        id: Unique identifier for the task
        title: Task title (required, non-empty after stripping whitespace)
        description: Task description (optional, defaults to empty string)
        completed: Completion status (default False)
        created_at: UTC timestamp when task was created
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        """
        Validates the title after initialization to ensure it's not empty after stripping whitespace.
        Sets the created_at timestamp if not provided.
        """
        # Validate title is not empty after stripping whitespace
        if not self.title.strip():
            raise ValueError("Task title cannot be empty or just whitespace")

        # Set creation timestamp if not provided
        if self.created_at is None:
            self.created_at = datetime.now()

    def __str__(self) -> str:
        """
        Returns a string representation of the task with status indicator.
        """
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.id}: {self.title}"