"""Integration tests to verify that users cannot access other users' tasks"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch
from src.main import app
from src.models.user import User
from src.models.task import Task
from src.database.database import get_session


# Create an in-memory SQLite database for testing
@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(engine):
    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_user_cannot_access_other_users_tasks(client: TestClient, session: Session):
    """Test that a user cannot access tasks belonging to another user"""

    # Create two users
    user1 = User(
        email="user1@example.com",
        name="User One",
        password="hashed_password_1"
    )
    user2 = User(
        email="user2@example.com",
        name="User Two",
        password="hashed_password_2"
    )

    session.add(user1)
    session.add(user2)
    session.commit()

    # Create a task for user1
    task_for_user1 = Task(
        title="User 1 Task",
        description="This belongs to user 1",
        completed=False,
        user_id=user1.id
    )

    session.add(task_for_user1)
    session.commit()

    # Mock JWT token validation to return user2's ID
    with patch("src.api.tasks.get_user_id_from_token") as mock_get_user_id:
        mock_get_user_id.return_value = str(user2.id)

        # Try to access user1's task as user2
        response = client.get(f"/api/tasks/{task_for_user1.id}")

        # Should return 404 (not found) or 403 (forbidden) - task shouldn't be accessible
        assert response.status_code in [403, 404]

        # Try to access all tasks as user2
        response = client.get("/api/tasks/")
        assert response.status_code == 200

        # User2 should see an empty list or only their own tasks (not user1's task)
        tasks = response.json()
        task_ids = [task['id'] for task in tasks]
        assert str(task_for_user1.id) not in task_ids


def test_user_can_access_own_tasks(client: TestClient, session: Session):
    """Test that a user can access their own tasks"""

    # Create a user
    user = User(
        email="ownuser@example.com",
        name="Own User",
        password="hashed_password"
    )
    session.add(user)
    session.commit()

    # Create a task for this user
    task = Task(
        title="Own Task",
        description="This belongs to the user",
        completed=False,
        user_id=user.id
    )
    session.add(task)
    session.commit()

    # Mock JWT token validation to return this user's ID
    with patch("src.api.tasks.get_user_id_from_token") as mock_get_user_id:
        mock_get_user_id.return_value = str(user.id)

        # Access the user's own task
        response = client.get(f"/api/tasks/{task.id}")
        assert response.status_code == 200

        # Access all tasks
        response = client.get("/api/tasks/")
        assert response.status_code == 200

        tasks = response.json()
        task_ids = [task['id'] for task in tasks]
        assert str(task.id) in task_ids