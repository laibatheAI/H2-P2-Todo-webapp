from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from typing import List
from ..database.database import get_session
from ..models.task import Task, TaskBase
from ..models.user import User
from ..services.task_service import (
    get_user_tasks, get_task_by_id, create_task,
    update_task, delete_task, toggle_task_completion
)
from ..services.jwt_service import verify_token, get_user_id_from_token
from pydantic import BaseModel

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

# Request/Response models
class TaskCreateRequest(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class TaskUpdateRequest(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

class TaskToggleResponse(BaseModel):
    id: str
    title: str
    description: str = None
    completed: bool
    user_id: str
    created_at: str
    updated_at: str

# Dependency to get current user from token
def get_current_user_token(authorization: str = Header(None)):
    """
    Dependency to extract and validate JWT token from Authorization header.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:]  # Remove "Bearer " prefix
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token

@router.get("/", response_model=List[Task])
def get_tasks(
    token: str = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    """
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    tasks = get_user_tasks(session, user_id)
    return tasks

@router.post("/", response_model=Task)
def create_new_task(
    task_data: TaskCreateRequest,
    token: str = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
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

    # Create the task - construct TaskBase with user_id from token
    task_to_create = TaskBase(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=user_id
    )
    db_task = create_task(session, task_to_create, user_id)
    return db_task

@router.get("/{task_id}", response_model=Task)
def get_specific_task(
    task_id: str,
    token: str = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    task = get_task_by_id(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return task

@router.put("/{task_id}", response_model=Task)
def update_existing_task(
    task_id: str,
    task_data: TaskUpdateRequest,
    token: str = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Update an existing task for the authenticated user.
    """
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validate title length if provided
    if task_data.title and (len(task_data.title) < 2 or len(task_data.title) > 50):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title should be in 2 to 50 characters"
        )

    # Validate description length if provided
    if task_data.description and len(task_data.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be less than 1000 characters"
        )

    # Construct TaskBase for update - use only the fields that are provided
    update_data = task_data.dict(exclude_unset=True)
    # Only include fields that exist in TaskBase (excluding user_id which is handled separately)
    task_base_fields = {"title", "description", "completed"}
    filtered_update_data = {k: v for k, v in update_data.items() if k in task_base_fields}
    # Add user_id to satisfy TaskBase validation
    filtered_update_data['user_id'] = user_id  # This will be overridden later in the service anyway

    updated_task = update_task(session, task_id, TaskBase(**filtered_update_data), user_id)
    return updated_task

@router.delete("/{task_id}")
def delete_specific_task(
    task_id: str,
    token: str = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Delete a task for the authenticated user.
    """
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    success = delete_task(session, task_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/toggle", response_model=Task)
def toggle_task_status(
    task_id: str,
    token: str = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task.
    """
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    toggled_task = toggle_task_completion(session, task_id, user_id)
    return toggled_task