import pytest
from httpx import AsyncClient

from training_tracker import security
from training_tracker.tests.helpers import create_distance


@pytest.mark.anyio
@pytest.mark.parametrize(
    "test_input, expected",
    [("Km", "km"), ("KM", "km"), ("km", "km"), ("kM", "km"), ("M", "m"), ("m", "m")],
)
async def test_create_distance(
    async_client: AsyncClient,
    confirmed_user: dict,
    logged_in_token: str,
    test_input: str,
    expected: str,
):
    distance = 1
    units = test_input
    response = await async_client.post(
        "/distance",
        json={"distance": distance, "units": units},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    assert {
        "id": 1,
        "distance": distance,
        "units": expected,
        "added_by_user_id": confirmed_user["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_distance_wrong_data(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/distance",
        json={},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_distance_expired_token(
    async_client: AsyncClient, mocker, confirmed_user: dict
):
    mocker.patch(
        "training_tracker.security.access_token_expiry_minutes", return_value=-1
    )
    token = security.create_access_token(confirmed_user["email"])
    response = await async_client.post(
        "/distance",
        json={"distance": 1, "units": "Kg"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_distance_already_exists(
    async_client: AsyncClient, logged_in_token: str, created_distance: dict
):
    distance = 1
    units = "Km"
    response = await async_client.post(
        "/distance",
        json={"distance": distance, "units": units},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 403


@pytest.mark.anyio
async def test_get_all_distances(async_client: AsyncClient, created_distance: dict):
    response = await async_client.get("/distances")
    assert response.status_code == 200
    assert created_distance.items() <= response.json()[0].items()


@pytest.mark.anyio
async def test_get_one_distance(async_client: AsyncClient, logged_in_token: str):
    await create_distance(1, "Km", async_client, logged_in_token)
    await create_distance(2, "Km", async_client, logged_in_token)
    response = await async_client.get("/distance/1")
    assert response.json()["distance"] == 1
    assert response.status_code == 200
