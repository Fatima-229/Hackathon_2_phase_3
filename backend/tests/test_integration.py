"""
Integration test to verify the full application functionality
"""
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


def test_full_application_flow():
    """
    Test the full application flow: register user -> login -> create task -> get task -> update task -> delete task
    """
    # Create an in-memory database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    
    with Session(engine) as session:
        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)
        
        # 1. Register a new user
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "integration@test.com",
                "password": "securepassword123"
            }
        )
        assert register_response.status_code == 200
        user_data = register_response.json()
        assert user_data["email"] == "integration@test.com"
        
        # 2. Login to get a token
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "integration@test.com",
                "password": "securepassword123"
            }
        )
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        
        # Store the token for authorization
        token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Create a task
        task_response = client.post(
            "/api/v1/tasks/",
            json={
                "title": "Integration Test Task",
                "description": "This is a test task for integration testing",
                "priority": "medium"
            },
            headers=headers
        )
        assert task_response.status_code == 200
        task_data = task_response.json()
        assert task_data["title"] == "Integration Test Task"
        assert task_data["description"] == "This is a test task for integration testing"
        assert task_data["priority"] == "medium"
        assert task_data["completed"] is False
        
        task_id = task_data["id"]
        
        # 4. Get all tasks
        get_tasks_response = client.get("/api/v1/tasks/", headers=headers)
        assert get_tasks_response.status_code == 200
        tasks_list = get_tasks_response.json()
        assert len(tasks_list) >= 1
        # Verify our task is in the list
        task_found = False
        for task in tasks_list:
            if task["id"] == task_id:
                task_found = True
                break
        assert task_found, "Created task should appear in the task list"
        
        # 5. Get specific task
        get_task_response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
        assert get_task_response.status_code == 200
        specific_task = get_task_response.json()
        assert specific_task["id"] == task_id
        assert specific_task["title"] == "Integration Test Task"
        
        # 6. Update the task
        update_response = client.put(
            f"/api/v1/tasks/{task_id}",
            json={
                "title": "Updated Integration Test Task",
                "description": "Updated description for integration testing",
                "priority": "high"
            },
            headers=headers
        )
        assert update_response.status_code == 200
        updated_task = update_response.json()
        assert updated_task["id"] == task_id
        assert updated_task["title"] == "Updated Integration Test Task"
        assert updated_task["priority"] == "high"
        
        # 7. Toggle task completion
        toggle_response = client.patch(f"/api/v1/tasks/{task_id}/complete", headers=headers)
        assert toggle_response.status_code == 200
        toggled_task = toggle_response.json()
        assert toggled_task["id"] == task_id
        assert toggled_task["completed"] is True  # Should now be completed
        
        # Toggle again to set it back to incomplete
        toggle_response2 = client.patch(f"/api/v1/tasks/{task_id}/complete", headers=headers)
        assert toggle_response2.status_code == 200
        toggled_task2 = toggle_response2.json()
        assert toggled_task2["id"] == task_id
        assert toggled_task2["completed"] is False  # Should now be incomplete again
        
        # 8. Delete the task
        delete_response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
        assert delete_response.status_code == 200
        
        # 9. Verify the task is deleted
        get_deleted_response = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
        assert get_deleted_response.status_code == 404
        
        # Clean up the override
        app.dependency_overrides.clear()
        
        print("All integration tests passed successfully!")


if __name__ == "__main__":
    test_full_application_flow()