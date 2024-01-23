from datetime import datetime
from httpx import AsyncClient


async def create_group(
    name: str, async_client: AsyncClient, logged_in_token: str
) -> dict:
    response = await async_client.post(
        "/group",
        json={"name": name},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def create_weight(
    weight: float, units: str, async_client: AsyncClient, logged_in_token: str
) -> dict:
    response = await async_client.post(
        "/weight",
        json={"weight": weight, "units": units},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def create_distance(
    distance: float, units: str, async_client: AsyncClient, logged_in_token: str
) -> dict:
    response = await async_client.post(
        "/distance",
        json={"distance": distance, "units": units},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def create_exercise(
    exercise_name: str, group_id: int, async_client: AsyncClient, logged_in_token: str
) -> dict:
    response = await async_client.post(
        "/exercise",
        json={"name": exercise_name, "group_id": group_id},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def create_set(
    async_client: AsyncClient,
    logged_in_token: str,
    exercise_count: int,
    exercise_id: int,
    training_id: int,
    distance_id: int = None,
    weight_id: int = None,
) -> dict:
    response = await async_client.post(
        "/set",
        json={
            "exercise_count": exercise_count,
            "exercise_id": exercise_id,
            "training_id": training_id,
            "distance_id": distance_id,
            "weight_id": weight_id,
        },
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def create_training(async_client: AsyncClient, logged_in_token, user_id: int, mocker) -> dict:
    mocker.patch("training_tracker.routers.trainings.get_current_date", return_value=datetime(2012, 3, 3, 10, 10, 10))
    mocker.patch("training_tracker.routers.trainings.get_current_user_id", return_value=user_id)
    response = await async_client.post(
        "/training",
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()
