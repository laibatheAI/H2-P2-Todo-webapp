"""
User scoping utilities for the Todo AI Chatbot application.
Provides functions for extracting user identity from JWT and enforcing user-level scoping.
"""
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from backend.middleware.auth import get_current_user_id, verify_user_owns_resource
from backend.models.task import Task
from backend.models.conversation import Conversation
from backend.models.message import Message


def get_user_id_from_request(request: Request) -> str:
    """
    Extract the authenticated user ID from the request.

    Args:
        request: FastAPI request object

    Returns:
        User ID string
    """
    return get_current_user_id(request)


def ensure_user_owns_task(db: Session, task_id: str, user_id: str) -> bool:
    """
    Ensure that the authenticated user owns the specified task.

    Args:
        db: Database session
        task_id: ID of the task to check
        user_id: ID of the authenticated user

    Returns:
        True if user owns the task, raises exception otherwise
    """
    try:
        # Validate task_id format
        UUID(task_id)
        UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID or user ID format"
        )

    # Query for the task with the specified ID
    task = db.query(Task).filter(Task.id == UUID(task_id)).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check if the task belongs to the authenticated user
    if str(task.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Task does not belong to authenticated user"
        )

    return True


def ensure_user_owns_conversation(db: Session, conversation_id: str, user_id: str) -> bool:
    """
    Ensure that the authenticated user owns the specified conversation.

    Args:
        db: Database session
        conversation_id: ID of the conversation to check
        user_id: ID of the authenticated user

    Returns:
        True if user owns the conversation, raises exception otherwise
    """
    try:
        # Validate conversation_id format
        UUID(conversation_id)
        UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID or user ID format"
        )

    # Query for the conversation with the specified ID
    conversation = db.query(Conversation).filter(Conversation.id == UUID(conversation_id)).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Check if the conversation belongs to the authenticated user
    if str(conversation.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Conversation does not belong to authenticated user"
        )

    return True


def ensure_user_owns_message(db: Session, message_id: str, user_id: str) -> bool:
    """
    Ensure that the authenticated user owns the specified message.

    Args:
        db: Database session
        message_id: ID of the message to check
        user_id: ID of the authenticated user

    Returns:
        True if user owns the message, raises exception otherwise
    """
    try:
        # Validate message_id format
        UUID(message_id)
        UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid message ID or user ID format"
        )

    # Query for the message with the specified ID
    message = db.query(Message).filter(Message.id == UUID(message_id)).first()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    # Check if the message belongs to the authenticated user
    if str(message.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Message does not belong to authenticated user"
        )

    return True


def get_user_tasks_query(db: Session, user_id: str):
    """
    Get a query for all tasks belonging to the specified user.

    Args:
        db: Database session
        user_id: ID of the user whose tasks to retrieve

    Returns:
        SQLAlchemy query for user's tasks
    """
    try:
        UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    return db.query(Task).filter(Task.user_id == UUID(user_id))


def get_user_conversations_query(db: Session, user_id: str):
    """
    Get a query for all conversations belonging to the specified user.

    Args:
        db: Database session
        user_id: ID of the user whose conversations to retrieve

    Returns:
        SQLAlchemy query for user's conversations
    """
    try:
        UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    return db.query(Conversation).filter(Conversation.user_id == UUID(user_id))


def get_user_messages_query(db: Session, user_id: str):
    """
    Get a query for all messages belonging to the specified user.

    Args:
        db: Database session
        user_id: ID of the user whose messages to retrieve

    Returns:
        SQLAlchemy query for user's messages
    """
    try:
        UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    return db.query(Message).filter(Message.user_id == UUID(user_id))


def get_user_filtered_tasks(db: Session, user_id: str, skip: int = 0, limit: int = 100, **filters):
    """
    Get tasks for a specific user with optional filtering.

    Args:
        db: Database session
        user_id: ID of the user whose tasks to retrieve
        skip: Number of tasks to skip for pagination
        limit: Maximum number of tasks to return
        **filters: Additional filters to apply (e.g., status, priority, category)

    Returns:
        List of user's tasks matching the criteria
    """
    try:
        UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    query = get_user_tasks_query(db, user_id)

    # Apply filters
    if 'status' in filters:
        if filters['status'] == 'completed':
            query = query.filter(Task.completed == True)
        elif filters['status'] == 'pending':
            query = query.filter(Task.completed == False)

    if 'priority' in filters:
        from backend.models.task import PriorityEnum
        query = query.filter(Task.priority == PriorityEnum(filters['priority']))

    if 'category' in filters:
        query = query.filter(Task.category == filters['category'])

    # Apply pagination
    tasks = query.offset(skip).limit(limit).all()
    return tasks


def get_user_filtered_conversations(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    """
    Get conversations for a specific user with optional filtering.

    Args:
        db: Database session
        user_id: ID of the user whose conversations to retrieve
        skip: Number of conversations to skip for pagination
        limit: Maximum number of conversations to return

    Returns:
        List of user's conversations
    """
    try:
        UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    query = get_user_conversations_query(db, user_id)

    # Apply pagination
    conversations = query.offset(skip).limit(limit).all()
    return conversations


def validate_user_scoping(model_instance: Any, user_id: str) -> bool:
    """
    Validate that a model instance belongs to the authenticated user.

    Args:
        model_instance: Instance of a model with a user_id attribute
        user_id: ID of the authenticated user

    Returns:
        True if instance belongs to user, False otherwise
    """
    try:
        UUID(user_id)
    except ValueError:
        return False

    if not hasattr(model_instance, 'user_id'):
        raise ValueError(f"Model instance {type(model_instance)} does not have a user_id attribute")

    instance_user_id = str(model_instance.user_id) if hasattr(model_instance.user_id, '__str__') else model_instance.user_id

    return instance_user_id == user_id


def validate_user_id_format(user_id: str) -> bool:
    """
    Validate that the provided user ID is in a valid UUID format.

    Args:
        user_id: User ID to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        UUID(user_id)
        return True
    except ValueError:
        return False


def get_user_isolation_error(user_id: str, resource_type: str, resource_id: str = None) -> HTTPException:
    """
    Create a standardized HTTP exception for user isolation violations.

    Args:
        user_id: ID of the user that attempted access
        resource_type: Type of resource that access was attempted for
        resource_id: ID of the resource that access was attempted for

    Returns:
        HTTPException with appropriate error message
    """
    resource_desc = f"{resource_type} {resource_id}" if resource_id else resource_type
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Access denied: {resource_desc} does not belong to authenticated user {user_id}"
    )