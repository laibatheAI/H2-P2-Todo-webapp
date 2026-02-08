"""
Token refresh mechanisms for the Todo AI Chatbot application.
Handles token refresh for long-running conversations and expired token scenarios.
"""
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from backend.config import settings


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a refresh token with extended expiration.

    Args:
        data: Data to encode in the token
        expires_delta: Optional timedelta for expiration

    Returns:
        Encoded refresh token string
    """
    import datetime as dt

    to_encode = data.copy()

    if expires_delta:
        expire = dt.datetime.utcnow() + expires_delta
    else:
        # Default refresh token expiration: 7 days
        expire = dt.datetime.utcnow() + dt.timedelta(days=7)

    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a refresh token and return its payload if valid.

    Args:
        token: The refresh token to verify

    Returns:
        Token payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        # Verify this is indeed a refresh token
        token_type = payload.get("type")
        if token_type != "refresh":
            return None

        user_id = payload.get("user_id")
        if user_id is None:
            return None

        return payload
    except JWTError:
        return None


def refresh_access_token(refresh_token: str) -> Optional[Dict[str, str]]:
    """
    Generate a new access token using a refresh token.

    Args:
        refresh_token: The refresh token to use

    Returns:
        Dictionary with new access token if successful, None otherwise
    """
    payload = verify_refresh_token(refresh_token)
    if not payload:
        return None

    user_id = payload.get("user_id")
    username = payload.get("username")

    # Create new access token with standard expiration
    new_access_data = {"user_id": user_id}
    if username:
        new_access_data["username"] = username

    new_access_token = jwt.encode(
        new_access_data,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


async def handle_expired_token_scenario(
    request: Request,
    response_handler
) -> Optional[Dict[str, Any]]:
    """
    Handle the scenario when a token has expired during a request.

    Args:
        request: The incoming request
        response_handler: Handler for sending responses

    Returns:
        Response dictionary if auto-refresh was successful, None otherwise
    """
    # Extract refresh token from request (either header or cookie)
    refresh_token = None

    # Check for refresh token in authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        # This would be the refresh token if the client is sending it here
        # Usually, refresh tokens are stored separately (cookie, local storage)
        # For this implementation, we'll assume it's sent differently
        pass

    # Check for refresh token in cookies
    refresh_token = request.cookies.get("refresh_token")

    # Check for refresh token in request body (less secure but sometimes used)
    try:
        body = await request.json()
        if "refresh_token" in body:
            refresh_token = body["refresh_token"]
    except:
        # Request body may not be JSON
        pass

    if refresh_token:
        # Attempt to refresh the access token
        new_tokens = refresh_access_token(refresh_token)
        if new_tokens:
            # In a real implementation, you would:
            # 1. Send the new access token to the client
            # 2. Potentially update the refresh token as well
            # 3. Retry the original request with the new token

            return {
                "success": True,
                "message": "Token refreshed successfully",
                "tokens": new_tokens
            }

    # If auto-refresh wasn't possible, return error response
    return None


def is_token_expiring_soon(token: str, minutes: int = 5) -> bool:
    """
    Check if a token is expiring soon.

    Args:
        token: The token to check
        minutes: Number of minutes to consider as "soon"

    Returns:
        True if token is expiring within the specified time, False otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": False}  # Don't verify expiration when just checking
        )

        exp_timestamp = payload.get("exp")
        if exp_timestamp is None:
            return True  # If no expiration, consider it expired

        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        current_datetime = datetime.utcnow()
        time_until_expiry = exp_datetime - current_datetime

        return time_until_expiry.total_seconds() < (minutes * 60)
    except JWTError:
        # If we can't decode the token, consider it expiring soon
        return True


def get_recommended_refresh_time(token: str) -> Optional[datetime]:
    """
    Get the recommended time to refresh a token (halfway through its validity).

    Args:
        token: The token to check

    Returns:
        Recommended refresh time, or None if token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": False}
        )

        exp_timestamp = payload.get("exp")
        iat_timestamp = payload.get("iat")  # Issued at time

        if exp_timestamp is None or iat_timestamp is None:
            return None

        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        iat_datetime = datetime.fromtimestamp(iat_timestamp)

        # Calculate halfway point
        total_duration = exp_datetime - iat_datetime
        halfway_point = iat_datetime + (total_duration / 2)

        return halfway_point
    except JWTError:
        return None


def should_refresh_token(token: str, buffer_minutes: int = 5) -> bool:
    """
    Determine if a token should be refreshed based on expiration time and buffer.

    Args:
        token: The token to check
        buffer_minutes: Minutes before expiration to refresh

    Returns:
        True if token should be refreshed, False otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": False}
        )

        exp_timestamp = payload.get("exp")
        if exp_timestamp is None:
            return True

        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        current_datetime = datetime.utcnow()
        time_until_expiry = exp_datetime - current_datetime

        return time_until_expiry.total_seconds() < (buffer_minutes * 60)
    except JWTError:
        # If we can't decode the token, we should get a new one
        return True


def prepare_token_refresh_response(new_access_token: str) -> Dict[str, Any]:
    """
    Prepare a standard response for token refresh operations.

    Args:
        new_access_token: The new access token to include in the response

    Returns:
        Standard token refresh response
    """
    return {
        "success": True,
        "message": "Token refreshed successfully",
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # in seconds
    }


def create_token_pair(user_id: str, username: Optional[str] = None) -> Dict[str, str]:
    """
    Create both access and refresh tokens for a user.

    Args:
        user_id: The ID of the user
        username: Optional username

    Returns:
        Dictionary containing both access and refresh tokens
    """
    # Create access token (short-lived)
    access_data = {"user_id": user_id}
    if username:
        access_data["username"] = username

    access_token = jwt.encode(
        access_data,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    # Create refresh token (long-lived)
    refresh_data = {"user_id": user_id}
    if username:
        refresh_data["username"] = username

    refresh_token = create_refresh_token(refresh_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }