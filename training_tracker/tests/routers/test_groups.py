import pytest
from httpx import AsyncClient
from training_tracker.tests.helpers import create_group
from training_tracker import security


@pytest.fixture()
async def created_group(async_client: AsyncClient, logged_in_token: str):
    return await create_group("Test group", async_client, logged_in_token)


@pytest.mark.anyio
async def test_create_group(
    async_client: AsyncClient, confirmed_user: dict, logged_in_token: str
):
    name = "Test group"
    response = await async_client.post(
        "/group",
        json={"name": name},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    assert {
        "id": 1,
        "name": name,
        "added_by_user_id": confirmed_user["id"],
    }.items() <= response.json().items()
    

@pytest.mark.anyio
async def test_create_group_wrong_data(async_client: AsyncClient, logged_in_token: str):
    response = await async_client.post(
        "/group",
        json={},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_group_expired_token(async_client: AsyncClient, mocker, confirmed_user: dict):
    mocker.patch("training_tracker.security.access_token_expiry_minutes", return_value=-1)
    token = security.create_access_token(confirmed_user["email"])
    response = await async_client.post(
        "/group",
        json={"name": "Test group"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_get_all_groups(async_client: AsyncClient, created_group: dict):
    response = await async_client.get("/groups")
    assert response.status_code == 200
    assert created_group.items() <= response.json()[0].items()
    

@pytest.mark.anyio
async def test_get_one_group(async_client: AsyncClient, logged_in_token:str):
    await create_group("Test group 1", async_client, logged_in_token)
    await create_group("Test group 2", async_client, logged_in_token)
    response = await async_client.get("/group/1")
    assert "Test group 1" in response.json()["name"]
    assert response.status_code == 200