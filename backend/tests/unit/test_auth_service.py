import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.auth import authenticate_user, register_user
from src.models.user import UserBase

@pytest.fixture
def mock_session():
    """Mock SQLModel session for testing"""
    session = Mock(spec=Session)
    return session

def test_authenticate_user_success(mock_session):
    """Test successful user authentication"""
    # Mock user data
    mock_user = Mock()
    mock_user.id = "123"
    mock_user.password = "$2b$12$LwiTee3tOmZJFf5q7W5z1O"  # Mock hashed password

    # Configure mock session to return the user
    mock_session.exec.return_value.first.return_value = mock_user

    # Patch the verify_password function to return True
    with patch('src.services.auth.verify_password', return_value=True):
        result = authenticate_user(mock_session, "test@example.com", "password123")

        assert result == mock_user
        mock_session.exec.assert_called_once()

def test_authenticate_user_wrong_password(mock_session):
    """Test authentication failure with wrong password"""
    # Mock user data
    mock_user = Mock()
    mock_user.id = "123"
    mock_user.password = "$2b$12$LwiTee3tOmZJFf5q7W5z1O"  # Mock hashed password

    # Configure mock session to return the user
    mock_session.exec.return_value.first.return_value = mock_user

    # Patch the verify_password function to return False
    with patch('src.services.auth.verify_password', return_value=False):
        result = authenticate_user(mock_session, "test@example.com", "wrongpassword")

        assert result is None

def test_authenticate_user_not_found(mock_session):
    """Test authentication failure when user doesn't exist"""
    # Configure mock session to return None
    mock_session.exec.return_value.first.return_value = None

    result = authenticate_user(mock_session, "nonexistent@example.com", "password123")

    assert result is None

def test_register_user_success(mock_session):
    """Test successful user registration"""
    user_data = UserBase(email="test@example.com", name="Test User", avatar=None)

    # Configure mock session to simulate successful save
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()

    # Mock the get_password_hash function
    with patch('src.services.auth.get_password_hash', return_value="hashed_password"):
        # Mock the User creation
        with patch('src.services.auth.User') as mock_user_class:
            mock_user_instance = Mock()
            mock_user_instance.id = "123"
            mock_user_instance.email = "test@example.com"
            mock_user_instance.name = "Test User"
            mock_user_class.return_value = mock_user_instance

            result = register_user(mock_session, user_data, "password123")

            # Verify the user was created with correct parameters
            mock_user_class.assert_called_once()
            mock_session.add.assert_called_once_with(mock_user_instance)
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_user_instance)

            assert result == mock_user_instance