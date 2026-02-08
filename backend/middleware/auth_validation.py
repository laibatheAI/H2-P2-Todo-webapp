"""
Authentication validation functions for the Todo AI Chatbot application.
Contains functions for validating JWT tokens and handling unauthorized scenarios.
"""
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime
from backend.config import settings
from backend.middleware.auth import jwt_auth, TokenData


def validate_access_token(token: str) -> Optional[TokenData]:
    """
    Validate an access token and return the token data if valid.

    Args:
        token: The JWT token string to validate

    Returns:
        TokenData object if valid, None if invalid
    """
    return jwt_auth.decode_token(token)


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired.

    Args:
        token: The JWT token string to check

    Returns:
        True if token is expired, False otherwise
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        exp_timestamp = payload.get("exp")

        if exp_timestamp is None:
            return True

        # Convert to datetime and compare with current time
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        current_datetime = datetime.utcnow()

        return current_datetime > exp_datetime
    except JWTError:
        # If there's an error decoding the token, treat it as expired
        return True


def validate_user_active_status(user_id: str) -> bool:
    """
    Validate that the user account is active.

    Note: In a real implementation, this would check against a user database.
    For this implementation, we'll assume all users are active.

    Args:
        user_id: The user ID to validate

    Returns:
        True if user is active, False otherwise
    """
    # In a real implementation, this would query the user database
    # to check if the account is active/enabled
    # For this example, we'll assume all users are active
    return True


def validate_token_scope(token_data: TokenData, required_scope: str = None) -> bool:
    """
    Validate that the token has the required scope.

    Args:
        token_data: The decoded token data
        required_scope: The scope required for the operation

    Returns:
        True if token has required scope, False otherwise
    """
    # In a real implementation, tokens would contain scope information
    # For this implementation, we'll assume all tokens have necessary scopes
    return True


def handle_unauthorized_access(detail: str = "Unauthorized access") -> HTTPException:
    """
    Create a standardized HTTP exception for unauthorized access.

    Args:
        detail: Specific detail message for the exception

    Returns:
        HTTPException with 401 status code
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def handle_forbidden_access(detail: str = "Access forbidden") -> HTTPException:
    """
    Create a standardized HTTP exception for forbidden access.

    Args:
        detail: Specific detail message for the exception

    Returns:
        HTTPException with 403 status code
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )


def validate_token_integrity(token: str) -> bool:
    """
    Perform comprehensive validation of token integrity.

    Args:
        token: The JWT token string to validate

    Returns:
        True if token is valid and intact, False otherwise
    """
    try:
        # Decode the token without verification to inspect claims
        unverified_payload = jwt.get_unverified_claims(token)

        # Check if required claims exist
        required_claims = ['user_id', 'exp']
        for claim in required_claims:
            if claim not in unverified_payload:
                return False

        # Now verify the token signature and expiration
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        # Check if token is expired
        exp_timestamp = payload.get("exp")
        if exp_timestamp is None:
            return False

        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        current_datetime = datetime.utcnow()
        if current_datetime > exp_datetime:
            return False

        return True
    except JWTError:
        return False


def get_token_from_request(request: Request) -> Optional[str]:
    """
    Extract the JWT token from the request Authorization header.

    Args:
        request: FastAPI request object

    Returns:
        Token string if found, None otherwise
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    return auth_header[len("Bearer "):]


def validate_authenticated_request(request: Request) -> TokenData:
    """
    Validate that the request is properly authenticated.

    Args:
        request: FastAPI request object

    Returns:
        TokenData object if request is validly authenticated

    Raises:
        HTTPException: If request is not properly authenticated
    """
    token = get_token_from_request(request)

    if not token:
        raise handle_unauthorized_access("Authorization token required in header")

    if is_token_expired(token):
        raise handle_unauthorized_access("Token has expired")

    token_data = validate_access_token(token)
    if not token_data:
        raise handle_unauthorized_access("Invalid token")

    # Additional validations
    if not validate_user_active_status(token_data.user_id):
        raise handle_unauthorized_access("User account is inactive")

    if not validate_token_integrity(token):
        raise handle_unauthorized_access("Token integrity check failed")

    return token_data


def validate_user_authorization(
    request: Request,
    resource_owner_id: str,
    action: str = "access"
) -> bool:
    """
    Validate that the authenticated user is authorized to perform an action on a resource.

    Args:
        request: FastAPI request object
        resource_owner_id: ID of the user who owns the resource
        action: Action being performed (e.g., "read", "write", "delete")

    Returns:
        True if user is authorized, raises exception if not
    """
    token_data = validate_authenticated_request(request)

    # Check if the authenticated user is the resource owner
    if token_data.user_id != resource_owner_id:
        raise handle_forbidden_access(
            f"Insufficient permissions to {action} resource owned by another user"
        )

    # Additional authorization checks could go here
    # For example, checking user roles, permissions, etc.

    return True


def refresh_access_token(refresh_token: str) -> Optional[Dict[str, str]]:
    """
    Generate a new access token using a refresh token.

    Args:
        refresh_token: The refresh token to use for generating new access token

    Returns:
        Dictionary with new access token if successful, None otherwise
    """
    # Note: In a real implementation, this would involve checking a refresh token database
    # For this implementation, we'll return None to indicate refresh functionality
    # would need to be implemented with proper refresh token storage and validation
    return None


def invalidate_token(token: str) -> bool:
    """
    Invalidate a token (add to blacklist in real implementation).

    Args:
        token: The token to invalidate

    Returns:
        True if token was invalidated, False otherwise
    """
    # In a real implementation, this would add the token to a blacklist/jti database
    # For this implementation, we'll just return True to indicate it's conceptually invalidated
    return True


def validate_token_audience(token: str, expected_audience: str) -> bool:
    """
    Validate that the token is intended for the expected audience.

    Args:
        token: The JWT token to validate
        expected_audience: The expected audience value

    Returns:
        True if token audience matches, False otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=expected_audience
        )
        return True
    except JWTError:
        # Audience mismatch or other validation error
        return False


def validate_token_issuer(token: str, expected_issuer: str) -> bool:
    """
    Validate that the token was issued by the expected issuer.

    Args:
        token: The JWT token to validate
        expected_issuer: The expected issuer value

    Returns:
        True if token issuer matches, False otherwise
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        issuer = payload.get("iss")
        return issuer == expected_issuer
    except JWTError:
        # Error decoding token or issuer doesn't match
        return False