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
    1. creates a tesk user
    2. creates a task with the test user's id as owner_id
    """

    # Create a test user in order to provide the test task with a valid owner_id
    user = {
        "user": {
            "name": "test user"
        }
    }
    user_response = await client.post("/api/users/create-user", json=user)
    user_data = user_response.json()
    user_id = user_data['result']['id']
    # Create the task
    task = {
        "task": {
            "name": "Testing the tests Task",
            "owner_id": user_id,
        }
    }
    response = await client.post("/api/tasks/create-task", json=task)
    assert response.status_code == 200
    task_data = response.json()
    task_result = task_data['result']
    assert task_result["name"] == task["task"]["name"]
    task_controller.remove_task(task_result["id"], override_get_db)
    user_controller.remove_user(override_get_db, user_id)


@pytest.mark.asyncio
async def test_edit_task(client: httpx.AsyncClient, override_get_db):
    """
    Test for task editting:
    1. creates a tesk user
    2. creates a task with the test user's id as owner_id
    3. updates the task
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
    response = await client.post(f"/api/tasks/edit/{task_id}", json=updated_task)
    assert response.status_code == 200
    task_data = response.json()
    task_result = task_data['result']
    assert task_result["name"] == updated_task["task"]["name"]

    # Remove the test user and task
    task_controller.remove_task(task_id, override_get_db)
    user_controller.remove_user(override_get_db, user_id)
