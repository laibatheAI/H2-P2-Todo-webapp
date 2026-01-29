from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from jwt import PyJWTError
from sqlmodel import Session
from fastapi import HTTPException, status
from ..models.user import User
import os
from dotenv import load_dotenv
import calendar
import time

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-jwt-key-here-make-it-long-and-random")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour as specified in requirements
REFRESH_TOKEN_EXPIRE_DAYS = 7    # 7 days as specified in requirements

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token with the specified expiration time.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Convert to Unix timestamp for JWT exp claim
    expire_timestamp = int(expire.timestamp())
    to_encode.update({"exp": expire_timestamp, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """
    Create a refresh token with a longer expiration time.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    # Convert to Unix timestamp for JWT exp claim
    expire_timestamp = int(expire.timestamp())
    to_encode.update({"exp": expire_timestamp, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Check if token is expired
        # The exp claim in JWT is a Unix timestamp (seconds since epoch)
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            if exp_timestamp < time.time():
                return None
        return payload
    except jwt.PyJWTError:  # Fixed: use jwt.PyJWTError instead of PyJWTError
        return None

def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from a JWT token.
    """
    payload = verify_token(token)
    if payload:
        return payload.get("sub")  # 'sub' is standard JWT claim for subject/user ID
    return None

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode an access token and return its payload if valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type = payload.get("type")
        if token_type != "access":
            return None
        # Also check if token is expired
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            if exp_timestamp < time.time():
                return None
        return payload
    except jwt.PyJWTError:  # Fixed: use jwt.PyJWTError instead of PyJWTError
        return None