import pytest
from httpx import AsyncClient

from training_tracker import security
from training_tracker.tests.helpers import create_set


@pytest.mark.anyio
async def test_create_set_with_distance(
    async_client: AsyncClient,
    confirmed_user: dict,
    logged_in_token: str,
    created_exercise: dict,
    created_training: dict,
    created_distance: dict,
):
    exercise_count = 15
    exercise_id = created_exercise["id"]
    training_id = created_training["id"]
    distance_id = created_distance["id"]
    response = await async_client.post(
        "/set",
        json={
            "exercise_count": exercise_count,
            "exercise_id": exercise_id,
            "training_id": training_id,
            "distance_id": distance_id,
        },
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    assert {
        "id": 1,
        "exercise_count": exercise_count,
        "exercise_id": exercise_id,
        "training_id": training_id,
        "distance_id": distance_id,
        "added_by_user_id": confirmed_user["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_set_with_weight(
    async_client: AsyncClient,
    confirmed_user: dict,
    logged_in_token: str,
    created_exercise: dict,
    created_training: dict,
    created_weight: dict,
):
    exercise_count = 15
    exercise_id = created_exercise["id"]
    training_id = created_training["id"]
    weight_id = created_weight["id"]
    response = await async_client.post(
        "/set",
        json={
            "exercise_count": exercise_count,
            "exercise_id": exercise_id,
            "training_id": training_id,
            "weight_id": weight_id,
        },
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    assert {
        "id": 1,
        "exercise_count": exercise_count,
        "exercise_id": exercise_id,
        "training_id": training_id,
        "weight_id": weight_id,
        "added_by_user_id": confirmed_user["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_set_wrong_data(async_client: AsyncClient, logged_in_token: str):
    response = await async_client.post(
        "/set",
        json={},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_set_expired_token(
    async_client: AsyncClient,
    mocker,
    confirmed_user: dict,
    created_exercise: dict,
    created_training: dict,
    created_distance: dict,
):
    exercise_count = 15
    exercise_id = created_exercise["id"]
    training_id = created_training["id"]
    distance_id = created_distance["id"]
    mocker.patch(
        "training_tracker.security.access_token_expiry_minutes", return_value=-1
    )
    token = security.create_access_token(confirmed_user["email"])
    response = await async_client.post(
        "/set",
        json={
            "exercise_count": exercise_count,
            "exercise_id": exercise_id,
            "training_id": training_id,
            "distance_id": distance_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_get_all_sets_with_distance(
    async_client: AsyncClient, created_set_with_distance: dict
):
    response = await async_client.get("/sets")
    assert response.status_code == 200
    assert created_set_with_distance.items() <= response.json()[0].items()


@pytest.mark.anyio
async def test_get_all_sets_with_weight(
    async_client: AsyncClient, created_set_with_weight: dict
):
    response = await async_client.get("/sets")
    assert response.status_code == 200
    assert created_set_with_weight.items() <= response.json()[0].items()


@pytest.mark.anyio
async def test_get_one_set(
    async_client: AsyncClient,
    logged_in_token: str,
    created_training,
    created_exercise,
    created_distance,
):
    exercise_counts = [20, 15, 10, 5]
    for i in exercise_counts:
        await create_set(
            async_client=async_client,
            logged_in_token=logged_in_token,
            exercise_count=i,
            exercise_id=created_exercise["id"],
            training_id=created_training["id"],
            distance_id=created_distance["id"],
        )
    response = await async_client.get("/set/1")
    assert response.json()["exercise_count"] == 20
    assert response.status_code == 200
