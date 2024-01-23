from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from training_tracker.database import database, distances
from training_tracker.models.schemas import Distance, DistanceIn, User
from training_tracker.security import get_current_user

router = APIRouter()


@router.post("/distance", response_model=Distance, status_code=201)
async def create_distance(
    distance: DistanceIn, current_user: Annotated[User, Depends(get_current_user)]
):
    dict_data = distance.model_dump()
    dict_data["units"] = dict_data.get("units").lower()
    existing_data = distances.select().where(
        (distances.c.distance == dict_data.get("distance"))
        & (distances.c.units == dict_data.get("units"))
    )
    res = await database.fetch_all(existing_data)
    if res:
        return JSONResponse(
            content={"message": "This weight is already exists"}, status_code=403
        )
    data = {**dict_data, "added_by_user_id": current_user.id}
    query = distances.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/distances", response_model=list[Distance])
async def get_all_weights():
    query = distances.select()
    return await database.fetch_all(query)


@router.get("/distance/{distance_id}", response_model=Distance)
async def get_distance_by_id(distance_id: int):
    query = distances.select().where(distances.c.id == distance_id)
    return await database.fetch_one(query)
