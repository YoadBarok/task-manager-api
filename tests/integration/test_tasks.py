from src.main import app
from typing import AsyncIterator
import httpx
import pytest
import pytest_asyncio
from src.app.api.controllers import task_controller
from src.app.api.controllers import user_controller


@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.mark.asyncio
async def test_all_tasks(client: httpx.AsyncClient) -> None:
    """
    Test for fetching all tasks
    """
    response = await client.get("/api/tasks/")
    assert response.status_code == 200
    assert response.json()['message'] == "Tasks fetched"


@pytest.mark.asyncio
async def test_create_task(client: httpx.AsyncClient, override_get_db):
    """
    Test for task creation:
    1. creates a test user
    2. creates a task with the test user's id as owner_id
    3. test for negative cases when task is created with non-existing user_id
    """
    # 1.
    # Create a test user in order to provide the test task with a valid owner_id
    user = {
        "user": {
            "name": "test user"
        }
    }
    user_response = await client.post("/api/users/create-user", json=user)
    user_data = user_response.json()
    user_id = user_data['result']['id']
    # 2.
    # Create the task
    task = {
        "task": {
            "name": "Testing the tests Task",
            "owner_id": user_id,
        }
    }
    passing_task = await client.post("/api/tasks/create-task", json=task)
    assert passing_task.status_code == 201
    task_data = passing_task.json()
    task_result = task_data['result']
    task_id = task_result['id']
    assert task_result["name"] == task["task"]["name"]
    delete_task = await client.delete(f"/api/tasks/delete/{task_id}")
    assert delete_task.status_code == 204
    delete_user = await client.delete(f"api/users/delete-user/{user_id}")
    assert delete_user.status_code == 204

    # 3.
    # Modify the task owner_id to a non existing owner_id, should return 400
    task["task"]["owner_id"] = 1000
    failing_task = await client.post("api/tasks/create-task", json=task)
    assert failing_task.status_code == 400


@pytest.mark.asyncio
async def test_edit_task(client: httpx.AsyncClient, override_get_db):
    """
    Test for task editting:
    1. creates a tesk user
    2. creates a task with the test user's id as owner_id
    3. updates the task
    4. test negative case with invalid task id
    """

    # Create a test user 
    user = {
        "user": {
            "name": "test user"
        }
    }
    user_response = await client.post("/api/users/create-user", json=user)
    user_data = user_response.json()
    user_id = user_data['result']['id']

    # Create the test task
    task = {
        "task": {
            "name": "Testing the tests Task",
            "owner_id": user_id,
        }
    }
    task_response = await client.post("/api/tasks/create-task", json=task)
    task_data = task_response.json()
    task_id = task_data['result']['id']

    # Edit the task
    updated_task = {
        "task": {
            "name": "Updated test task name",
            "owner_id": user_id
        }
    }
    passing_edit = await client.post(f"/api/tasks/edit/{task_id}", json=updated_task)
    assert passing_edit.status_code == 200
    task_data = passing_edit.json()
    task_result = task_data['result']
    assert task_result["name"] == updated_task["task"]["name"]

    # Try to edit a non existing task
    failing_edit = await client.post(f"/api/tasks/edit/2000", json=updated_task)
    assert failing_edit.status_code == 404

    # Remove the test user and task
    task_controller.remove_task(task_id, override_get_db)
    user_controller.remove_user(override_get_db, user_id)
