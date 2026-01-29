from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from typing import Dict, Any, Optional
from ..database.database import get_session
from ..models.user import User, UserBase
from ..services.auth import register_user, authenticate_user, create_auth_tokens, register_user_async, authenticate_user_async
from ..services.jwt_service import verify_token, get_user_id_from_token
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Request/Response models
class UserRegistrationRequest(BaseModel):
    email: str
    password: str
    name: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    avatar: Optional[str] = None
    created_at: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse

class LogoutResponse(BaseModel):
    message: str

@router.post("/register", response_model=dict)
async def register(
    user_data: UserRegistrationRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user with email, password, and name.
    """
    try:
        # Create user using the auth service
        from ..models.user import UserBase
        from ..services.auth import register_user_async
        db_user = await register_user_async(
            session=session,
            user_data=UserBase(
                email=user_data.email,
                name=user_data.name,
                avatar=None  # Avatar can be set later
            ),
            password=user_data.password
        )

        # Create auth tokens
        from ..services.auth import create_auth_tokens
        tokens = create_auth_tokens(str(db_user.id))

        return {
            "id": str(db_user.id),
            "email": db_user.email,
            "name": db_user.name,
            "created_at": db_user.created_at.isoformat(),
            **tokens
        }
    except HTTPException:
        # Re-raise HTTP exceptions from the service layer
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate user with email and password, return JWT tokens.
    """
    from ..services.auth import authenticate_user_async
    user = await authenticate_user_async(
        session=session,
        email=login_data.email,
        password=login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create auth tokens
    from ..services.auth import create_auth_tokens
    tokens = create_auth_tokens(str(user.id))

    # Format response
    user_response = UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        created_at=user.created_at.isoformat()
    )

    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"],
        user=user_response
    )

@router.post("/logout")
def logout():
    """
    Logout endpoint (client-side token removal is sufficient)
    """
    return {"message": "Logged out successfully"}

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

@router.get("/me", response_model=UserResponse)
def get_current_user(
    token: str = Depends(get_current_user_token),
    session: Session = Depends(get_session)
):
    """
    Get current authenticated user's information.
    """
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        avatar=user.avatar,
        created_at=user.created_at.isoformat()
    )