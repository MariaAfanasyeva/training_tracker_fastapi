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
