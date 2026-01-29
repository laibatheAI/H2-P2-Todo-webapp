from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List, Optional
import uuid
from ..models.task import Task, TaskBase
from ..models.user import User

def get_user_tasks(session: Session, user_id: str) -> List[Task]:
    """
    Get all tasks for a specific user.
    """
    try:
        user_uuid = uuid.UUID(user_id)
        statement = select(Task).where(Task.user_id == user_uuid)
        tasks = session.exec(statement).all()
        return tasks
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

def get_task_by_id(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a specific user.
    """
    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)
        statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        task = session.exec(statement).first()
        return task
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task or user ID format"
        )

def create_task(session: Session, task_data: TaskBase, user_id: str) -> Task:
    """
    Create a new task for a specific user.
    """
    try:
        user_uuid = uuid.UUID(user_id)

        # Verify that the user exists
        user_statement = select(User).where(User.id == user_uuid)
        user = session.exec(user_statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Validate title length (2-50 characters)
        if len(task_data.title) < 2 or len(task_data.title) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task title should be in 2 to 50 characters"
            )

        # Validate description length (max 1000 characters)
        if task_data.description and len(task_data.description) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be less than 1000 characters"
            )

        # Create the task
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            user_id=user_uuid
        )

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

def update_task(session: Session, task_id: str, task_data: TaskBase, user_id: str) -> Task:
    """
    Update an existing task for a specific user.
    """
    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)

        # Get the existing task
        statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        db_task = session.exec(statement).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        # Validate title length (2-50 characters)
        if task_data.title and (len(task_data.title) < 2 or len(task_data.title) > 50):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task title should be in 2 to 50 characters"
            )

        # Validate description length (max 1000 characters)
        if task_data.description and len(task_data.description) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be less than 1000 characters"
            )

        # Update the task fields
        if task_data.title is not None:
            db_task.title = task_data.title
        if task_data.description is not None:
            db_task.description = task_data.description
        if task_data.completed is not None:
            db_task.completed = task_data.completed

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task or user ID format"
        )

def delete_task(session: Session, task_id: str, user_id: str) -> bool:
    """
    Delete a task for a specific user.
    """
    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)

        # Get the existing task
        statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        db_task = session.exec(statement).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        session.delete(db_task)
        session.commit()
        return True
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task or user ID format"
        )

def toggle_task_completion(session: Session, task_id: str, user_id: str) -> Task:
    """
    Toggle the completion status of a task.
    """
    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)

        # Get the existing task
        statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        db_task = session.exec(statement).first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        # Toggle the completion status
        db_task.completed = not db_task.completed

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task or user ID format"
        )