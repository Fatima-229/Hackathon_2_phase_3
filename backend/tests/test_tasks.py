import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from backend.main import app
from backend.database import get_session
from backend.models.user import User
from backend.models.task import Task
from backend.utils.security import get_password_hash
from uuid import uuid4
from datetime import datetime


# Create a test database engine
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(client: TestClient, session: Session):
    # Create a test user
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        created_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Get a token for the user (we'll simulate this since we can't easily authenticate)
    # For testing purposes, we'll bypass authentication by overriding the dependency
    from backend.models.user import User as UserModel
    
    def get_current_user_override():
        return user

    # Import here to avoid circular import issues
    from backend.utils.auth import get_current_user
    app.dependency_overrides[get_current_user] = get_current_user_override
    
    yield client
    
    # Clean up the override
    app.dependency_overrides.pop(get_current_user)


def test_create_task(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "priority": "medium"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["priority"] == "medium"
    assert data["completed"] is False
    # Verify that the user_id is set correctly
    # Since we're mocking the authentication, we can't verify the exact user_id


def test_get_tasks(authenticated_client: TestClient):
    # Create a task first
    authenticated_client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "priority": "medium"
        }
    )
    
    response = authenticated_client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Test Task"


def test_get_task_by_id(authenticated_client: TestClient):
    # Create a task first
    create_response = authenticated_client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "priority": "medium"
        }
    )
    task_id = create_response.json()["id"]
    
    response = authenticated_client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"


def test_update_task(authenticated_client: TestClient):
    # Create a task first
    create_response = authenticated_client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "priority": "medium"
        }
    )
    task_id = create_response.json()["id"]
    
    response = authenticated_client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "description": "Updated Description",
            "priority": "high"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert data["priority"] == "high"


def test_toggle_task_completion(authenticated_client: TestClient):
    # Create a task first
    create_response = authenticated_client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "priority": "medium"
        }
    )
    task_id = create_response.json()["id"]
    
    # Initially task should not be completed
    response = authenticated_client.get(f"/api/v1/tasks/{task_id}")
    assert response.json()["completed"] is False
    
    # Toggle completion
    response = authenticated_client.patch(f"/api/v1/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    
    # Toggle again to make sure it works both ways
    response = authenticated_client.patch(f"/api/v1/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False


def test_delete_task(authenticated_client: TestClient):
    # Create a task first
    create_response = authenticated_client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task to Delete",
            "description": "Test Description",
            "priority": "medium"
        }
    )
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = authenticated_client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    
    # Verify the task is gone
    response = authenticated_client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 404