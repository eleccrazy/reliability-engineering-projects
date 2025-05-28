"""
File: test_tasks.py
Description: Unit tests for task management API using FastAPI and SQLAlchemy.
Author: Gizachew Kassa
Date Created: 2025-05-28
"""

import pytest
from fastapi.testclient import TestClient

# client is provided by conftest.py as a fixture


def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Management API"}


def test_create_task(client: TestClient):
    response = client.post("/tasks/", json={"name": "Write tests", "completed": False})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Write tests"
    assert data["completed"] is False
    assert "id" in data


def test_read_tasks(client: TestClient):
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert any("id" in task for task in tasks)


def test_read_single_task(client: TestClient):
    create = client.post("/tasks/", json={"name": "Read me", "completed": False})
    task_id = create.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == task_id
    assert task["name"] == "Read me"


def test_update_task(client: TestClient):
    create = client.post("/tasks/", json={"name": "Old Task", "completed": False})
    task_id = create.json()["id"]

    update = client.put(
        f"/tasks/{task_id}", json={"name": "Updated Task", "completed": True}
    )
    assert update.status_code == 200
    task = update.json()
    assert task["name"] == "Updated Task"
    assert task["completed"] is True


def test_delete_task(client: TestClient):
    create = client.post("/tasks/", json={"name": "To be deleted", "completed": False})
    task_id = create.json()["id"]

    delete = client.delete(f"/tasks/{task_id}")
    assert delete.status_code == 200
    assert delete.json() == {"message": "Task deleted"}

    confirm = client.get(f"/tasks/{task_id}")
    assert confirm.status_code == 404
