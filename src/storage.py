from typing import List, Optional
from .models import Task


class TaskManager:
    """
    Manages tasks in-memory with CRUD operations.
    """

    def __init__(self):
        """
        Initialize with empty task list and ID counter.
        """
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add new task to collection, return created Task object.

        Args:
            title: Task title (required, non-empty after stripping)
            description: Task description (optional, defaults to empty string)

        Returns:
            Task: The newly created Task object

        Raises:
            ValueError: If title is empty after stripping whitespace
        """
        # Validate title is not empty after stripping whitespace
        if not title.strip():
            raise ValueError("Task title cannot be empty or just whitespace")

        # Create task with auto-incremented ID
        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description.strip() if description else "",
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> List[Task]:
        """
        Return all tasks in collection, sorted by creation order (oldest first).

        Returns:
            List[Task]: All tasks in the collection, sorted by ID (creation order)
        """
        return self._tasks.copy()  # Return a copy to prevent external modification

    def get_task(self, task_id: int) -> Task:
        """
        Return specific task by ID, raises ValueError if not found.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task: The task with the specified ID

        Raises:
            ValueError: If no task with the given ID exists
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task with ID {task_id} not found")

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """
        Update specific task fields, return updated Task object.

        Args:
            task_id: The ID of the task to update
            title: New title (optional, if None then field is unchanged)
            description: New description (optional, if None then field is unchanged)

        Returns:
            Task: The updated Task object

        Raises:
            ValueError: If no task with the given ID exists or if title is provided but is empty after stripping
        """
        task = self.get_task(task_id)

        # Validate new title if provided
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty or just whitespace")
            task.title = title.strip()

        # Update description if provided
        if description is not None:
            task.description = description.strip() if description else ""

        return task

    def toggle_complete(self, task_id: int) -> Task:
        """
        Toggle completion status of task, return updated Task object.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            Task: The task with toggled completion status

        Raises:
            ValueError: If no task with the given ID exists
        """
        task = self.get_task(task_id)
        task.completed = not task.completed
        return task

    def delete_task(self, task_id: int) -> None:
        """
        Remove task from collection, raises ValueError if not found.

        Args:
            task_id: The ID of the task to delete

        Raises:
            ValueError: If no task with the given ID exists
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return
        raise ValueError(f"Task with ID {task_id} not found")