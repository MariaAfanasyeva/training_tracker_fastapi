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