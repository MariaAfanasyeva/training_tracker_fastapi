import pytest
from httpx import AsyncClient


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
    # assert response.status_code == 201
    assert {
        "id": 1,
        "name": name,
        "added_by_user_id": confirmed_user["id"],
    }.items() <= response.json().items()
