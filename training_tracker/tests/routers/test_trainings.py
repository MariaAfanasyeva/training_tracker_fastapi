from datetime import datetime
import pytest
from httpx import AsyncClient

from training_tracker import security
from training_tracker.tests.helpers import create_training


@pytest.mark.anyio
async def test_create_training(async_client: AsyncClient, confirmed_user: dict, logged_in_token: str, mocker):
    mocker.patch("training_tracker.routers.trainings.get_current_date", return_value=datetime(2012, 3, 3, 10, 10, 10))
    response = await async_client.post(
        "/training",
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    assert {
        "id": 1,
        "user_id": confirmed_user["id"],
        "training_date": "2012-03-03T10:10:10",
        "status": "Started"
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_training_expired_token(
    async_client: AsyncClient, mocker, confirmed_user: dict
):
    mocker.patch(
        "training_tracker.security.access_token_expiry_minutes", return_value=-1
    )
    token = security.create_access_token(confirmed_user["email"])
    response = await async_client.post(
        "/training",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]
    
    
@pytest.mark.anyio
async def test_get_all_trainings_for_user(async_client: AsyncClient, confirmed_user: dict, logged_in_token: str, mocker):
    for _ in range(4):
        await create_training(async_client, logged_in_token, confirmed_user["id"], mocker)
    await create_training(async_client, logged_in_token, 2, mocker)
    mocker.patch("training_tracker.routers.trainings.get_current_user_id", return_value=confirmed_user["id"])
    response = await async_client.get("/trainings", headers={"Authorization": f"Bearer {logged_in_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 4
    
    
@pytest.mark.anyio
async def test_get_all_trainings_for_user_no_items(async_client: AsyncClient, confirmed_user: dict, logged_in_token: str, mocker):
    for _ in range(4):
        await create_training(async_client, logged_in_token, 4, mocker)
    mocker.patch("training_tracker.routers.trainings.get_current_user_id", return_value=confirmed_user["id"])
    response = await async_client.get("/trainings", headers={"Authorization": f"Bearer {logged_in_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 0
    

@pytest.mark.anyio
async def test_get_training_by_id_for_user(async_client: AsyncClient, confirmed_user: dict, logged_in_token: str, mocker):
    for _ in range(4):
        await create_training(async_client, logged_in_token, confirmed_user["id"], mocker)
    await create_training(async_client, logged_in_token, 2, mocker)
    mocker.patch("training_tracker.routers.trainings.get_current_user_id", return_value=confirmed_user["id"])
    response = await async_client.get("/training/2", headers={"Authorization": f"Bearer {logged_in_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == 2


@pytest.mark.anyio
async def test_get_training_by_wrong_id_for_user(async_client: AsyncClient, confirmed_user: dict, logged_in_token: str, mocker):
    for _ in range(3):
        await create_training(async_client, logged_in_token, confirmed_user["id"], mocker)
    await create_training(async_client, logged_in_token, 2, mocker)
    mocker.patch("training_tracker.routers.trainings.get_current_user_id", return_value=confirmed_user["id"])
    response = await async_client.get("/training/4", headers={"Authorization": f"Bearer {logged_in_token}"})
    assert response.status_code == 403
