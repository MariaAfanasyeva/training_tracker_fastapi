import pytest
from httpx import AsyncClient

from training_tracker import security
from training_tracker.tests.helpers import create_exercise


@pytest.mark.anyio
async def test_create_exercise(
    async_client: AsyncClient,
    confirmed_user: dict,
    logged_in_token: str,
    created_group: dict,
):
    name = "Test exercise"
    group_id = created_group["id"]
    response = await async_client.post(
        "/exercise",
        json={"name": name, "group_id": group_id},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    assert {
        "id": 1,
        "name": name,
        "group_id": group_id,
        "added_by_user_id": confirmed_user["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_exercise_wrong_data(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/exercise",
        json={},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_exercise_expired_token(
    async_client: AsyncClient, mocker, confirmed_user: dict, created_group: dict
):
    mocker.patch(
        "training_tracker.security.access_token_expiry_minutes", return_value=-1
    )
    token = security.create_access_token(confirmed_user["email"])
    name = "Test exercise"
    group_id = created_group["id"]
    response = await async_client.post(
        "/exercise",
        json={"name": name, "group_id": group_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_exercise_already_exists(
    async_client: AsyncClient,
    logged_in_token: str,
    created_exercise: dict,
    created_group: dict,
):
    name = "Test name"
    group_id = created_group["id"]
    response = await async_client.post(
        "/exercise",
        json={"name": name, "group_id": group_id},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_all_exercises(async_client: AsyncClient, created_exercise: dict):
    response = await async_client.get("/exercises")
    assert response.status_code == 200
    assert created_exercise.items() <= response.json()[0].items()


@pytest.mark.anyio
async def test_get_one_exercise(async_client: AsyncClient, logged_in_token: str):
    await create_exercise("Test exercise 1", 1, async_client, logged_in_token)
    await create_exercise("Test exercise 2", 1, async_client, logged_in_token)
    response = await async_client.get("/exercise/1")
    assert "Test exercise 1" in response.json()["name"]
    assert response.status_code == 200
