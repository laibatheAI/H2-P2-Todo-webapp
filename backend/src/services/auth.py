from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import Optional
from datetime import timedelta
import uuid
from ..models.user import User, UserBase
from ..services.jwt_service import create_access_token, create_refresh_token, verify_token
from passlib.context import CryptContext
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create a thread pool executor for CPU-bound operations like password hashing
executor = ThreadPoolExecutor(max_workers=4)

def verify_password_sync(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Async wrapper for password verification to run in thread pool.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, verify_password_sync, plain_password, hashed_password)

def get_password_hash_sync(password: str) -> str:
    """
    Hash a plain password.
    """
    return pwd_context.hash(password)

async def get_password_hash(password: str) -> str:
    """
    Async wrapper for password hashing to run in thread pool.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, get_password_hash_sync, password)

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    NOTE: This is kept sync because it's used in sync context in the API layer.
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user or not verify_password_sync(password, user.password):
        return None
    return user

async def authenticate_user_async(session: Session, email: str, password: str) -> Optional[User]:
    """
    Async version of authenticate_user to prevent blocking during password verification.
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user:
        return None

    # Verify password asynchronously to prevent blocking the event loop
    loop = asyncio.get_event_loop()
    is_valid = await loop.run_in_executor(None, verify_password_sync, password, user.password)

    if not is_valid:
        return None
    return user

def register_user(session: Session, user_data: UserBase, password: str) -> User:
    """
    Register a new user with hashed password.
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password using sync version to maintain compatibility with sync API
    hashed_password = get_password_hash_sync(password)

    # Create new user
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        avatar=user_data.avatar,
        password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

async def register_user_async(session: Session, user_data: UserBase, password: str) -> User:
    """
    Async version of register_user to prevent blocking during password hashing.
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password asynchronously to prevent blocking the event loop
    loop = asyncio.get_event_loop()
    hashed_password = await loop.run_in_executor(None, get_password_hash_sync, password)

    # Create new user
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        avatar=user_data.avatar,
        password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def create_auth_tokens(user_id: str) -> dict:
    """
    Create access and refresh tokens for a user.
    """
    from datetime import timedelta
    access_token_expires = timedelta(minutes=60)  # 1 hour
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user_id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def refresh_access_token(refresh_token: str) -> Optional[dict]:
    """
    Refresh an access token using a refresh token.
    """
    try:
        import jwt
        from ..services.jwt_service import SECRET_KEY, ALGORITHM
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type = payload.get("type")
        if token_type != "refresh":
            return None

        # Extract user ID and create new access token
        user_id = payload.get("sub")
        if not user_id:
            return None

        # Create new access token
        from ..services.jwt_service import create_access_token
        new_access_token = create_access_token(data={"sub": user_id})
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except jwt.PyJWTError:
        return None

def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    """
    Get a user by their ID.
    """
    try:
        uuid_obj = uuid.UUID(user_id)
        statement = select(User).where(User.id == uuid_obj)
        user = session.exec(statement).first()
        return user
    except ValueError:
        # Invalid UUID format
        return None