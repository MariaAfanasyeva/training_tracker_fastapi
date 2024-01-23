import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

os.environ["ENV_STATE"] = "test"

from training_tracker.database import database, engine, metadata, users  # noqa: E402
from training_tracker.main import app  # noqa: E402
from training_tracker.tests.helpers import ( # noqa: E402
    create_distance,  
    create_exercise,
    create_group,
    create_set,
    create_training,
    create_weight,
)

metadata.create_all(engine)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield database
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.com", "password": "1234"}
    await async_client.post("/register", json=user_details)
    query = users.select().where(users.c.email == user_details["email"])
    user = await database.fetch_one(query)
    user_details["id"] = user.id
    return user_details


@pytest.fixture()
async def confirmed_user(registered_user: dict) -> dict:
    query = (
        users.update()
        .where(users.c.email == registered_user["email"])
        .values(confirmed=True)
    )
    await database.execute(query)
    return registered_user


@pytest.fixture()
async def logged_in_token(async_client: AsyncClient, confirmed_user: dict) -> str:
    response = await async_client.post("/token", json=confirmed_user)
    return response.json()["access_token"]


@pytest.fixture()
async def created_group(async_client: AsyncClient, logged_in_token: str):
    return await create_group("Test group", async_client, logged_in_token)


@pytest.fixture()
async def created_distance(async_client: AsyncClient, logged_in_token: str):
    return await create_distance(1, "Km", async_client, logged_in_token)


@pytest.fixture()
async def created_exercise(
    async_client: AsyncClient, logged_in_token: str, created_group: dict
):
    return await create_exercise(
        "Test name", created_group["id"], async_client, logged_in_token
    )


@pytest.fixture()
async def created_weight(async_client: AsyncClient, logged_in_token: str):
    return await create_weight(1, "Kg", async_client, logged_in_token)


@pytest.fixture()
async def created_training(async_client: AsyncClient, logged_in_token: str, mocker):
    return await create_training(async_client, logged_in_token, 1, mocker)


@pytest.fixture
async def created_set_with_distance(
    async_client: AsyncClient,
    logged_in_token: str,
    created_exercise: dict,
    created_training: dict,
    created_distance: dict,
):
    return await create_set(
        async_client=async_client,
        logged_in_token=logged_in_token,
        exercise_count=15,
        exercise_id=created_exercise["id"],
        training_id=created_training["id"],
        distance_id=created_distance["id"],
    )


@pytest.fixture
async def created_set_with_weight(
    async_client: AsyncClient,
    logged_in_token: str,
    created_exercise: dict,
    created_training: dict,
    created_weight: dict,
):
    return await create_set(
        async_client=async_client,
        logged_in_token=logged_in_token,
        exercise_count=20,
        exercise_id=created_exercise["id"],
        training_id=created_training["id"],
        weight_id=created_weight["id"],
    )
