from fastapi import HTTPException, status, Header
from ..services.jwt_service import verify_token, get_user_id_from_token
from ..models.user import User
from sqlmodel import Session, select
from ..database.database import get_session

def verify_jwt_token(authorization: str = Header(None)):
    """
    Verify JWT token from Authorization header and return the token if valid.
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

def get_current_user_id(authorization: str = Header(None)) -> str:
    """
    Extract and verify user ID from JWT token in Authorization header.
    """
    token = verify_jwt_token(authorization)
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id

def validate_user_owns_resource(session: Session, user_id: str, resource_user_id: str):
    """
    Validate that the authenticated user owns the resource they're trying to access.
    """
    if user_id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You don't have permission to access this resource"
        )