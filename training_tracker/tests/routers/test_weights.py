import pytest
from httpx import AsyncClient

from training_tracker import security
from training_tracker.tests.helpers import create_weight


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_input, expected",
    [("Kg", "kg"), ("KG", "kg"), ("kg", "kg"), ("kG", "kg"), ("G", "g"), ("g", "g")],
)
async def test_create_weight(
    async_client: AsyncClient,
    confirmed_user: dict,
    logged_in_token: str,
    test_input: str,
    expected: str,
):
    weight = 1
    units = test_input
    response = await async_client.post(
        "/weight",
        json={"weight": weight, "units": units},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    assert {
        "id": 1,
        "weight": weight,
        "units": expected,
        "added_by_user_id": confirmed_user["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_weight_wrong_data(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/weight",
        json={},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_weight_expired_token(
    async_client: AsyncClient, mocker, confirmed_user: dict
):
    mocker.patch(
        "training_tracker.security.access_token_expiry_minutes", return_value=-1
    )
    token = security.create_access_token(confirmed_user["email"])
    response = await async_client.post(
        "/weight",
        json={"weigth": 1, "units": "Kg"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_weight_already_exists(
    async_client: AsyncClient, logged_in_token: str, created_weight: dict
):
    weight = 1
    units = "Kg"
    response = await async_client.post(
        "/weight",
        json={"weight": weight, "units": units},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_all_weights(async_client: AsyncClient, created_weight: dict):
    response = await async_client.get("/weights")
    assert response.status_code == 200
    assert created_weight.items() <= response.json()[0].items()


@pytest.mark.anyio
async def test_get_one_weight(async_client: AsyncClient, logged_in_token: str):
    await create_weight(1, "Kg", async_client, logged_in_token)
    await create_weight(2, "Kg", async_client, logged_in_token)
    response = await async_client.get("/weight/1")
    assert response.json()["weight"] == 1
    assert response.status_code == 200
