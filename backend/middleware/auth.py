"""
Authentication middleware for the Todo AI Chatbot application.
Handles JWT token validation and user identity extraction.
"""
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
from functools import wraps
from backend.config import settings
from uuid import UUID


class TokenData(BaseModel):
    """Model for token payload data."""
    user_id: str
    username: Optional[str] = None


class JWTAuth:
    """JWT authentication class for handling token validation and user identification."""

    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.security = HTTPBearer()

    def decode_token(self, token: str) -> Optional[TokenData]:
        """
        Decode and validate a JWT token.

        Args:
            token: The JWT token string

        Returns:
            TokenData object if valid, None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("user_id")
            username: str = payload.get("username")

            if user_id is None:
                return None

            token_data = TokenData(user_id=user_id, username=username)
            return token_data
        except JWTError:
            return None

    def validate_token(self, credentials: HTTPAuthorizationCredentials = None) -> TokenData:
        """
        Validate the provided token and raise an exception if invalid.

        Args:
            credentials: HTTP authorization credentials

        Returns:
            TokenData object if valid

        Raises:
            HTTPException: If token is invalid or missing
        """
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = credentials.credentials
        token_data = self.decode_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return token_data

    async def __call__(self, request: Request) -> TokenData:
        """
        Async call method to validate JWT token in requests.

        Args:
            request: FastAPI request object

        Returns:
            TokenData object with user information
        """
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or malformed",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header[len("Bearer "):]
        token_data = self.decode_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Add token data to request state for use in route handlers
        request.state.user_id = token_data.user_id
        request.state.username = token_data.username

        return token_data


# Initialize JWT authentication instance
jwt_auth = JWTAuth()


def get_current_user_id(request: Request) -> str:
    """
    Get the current user ID from the request state.

    Args:
        request: FastAPI request object

    Returns:
        User ID string
    """
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in request state",
        )
    return user_id


def require_authentication():
    """
    Decorator to require authentication for route handlers.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # The middleware should have already validated the token
            # and added user info to request.state
            request = kwargs.get('request') or next((arg for arg in args if isinstance(arg, Request)), None)

            if not request or not hasattr(request.state, 'user_id'):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator


def verify_user_owns_resource(user_id: str, resource_user_id: str) -> bool:
    """
    Verify that the authenticated user owns the specified resource.

    Args:
        user_id: The ID of the authenticated user
        resource_user_id: The user ID associated with the resource

    Returns:
        True if user owns the resource, False otherwise
    """
    try:
        # Validate both are valid UUIDs
        UUID(user_id)
        UUID(resource_user_id)

        return user_id == resource_user_id
    except ValueError:
        # If either is not a valid UUID, they don't match
        return False


def get_user_scoped_query(base_query, model_class, user_id: str):
    """
    Apply user scoping to a SQLAlchemy query to ensure data isolation.

    Args:
        base_query: The base query to apply scoping to
        model_class: The model class being queried
        user_id: The ID of the authenticated user

    Returns:
        Query with user scoping applied
    """
    # Assuming the model has a user_id field for scoping
    # This is a simplified version - in practice, you'd need to check if the field exists
    return base_query.filter(model_class.user_id == user_id)


def create_access_token(data: dict, expires_delta=None) -> str:
    """
    Create a new JWT access token.

    Args:
        data: Dictionary containing the token data
        expires_delta: Optional timedelta for token expiration

    Returns:
        Encoded JWT token string
    """
    import datetime

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt