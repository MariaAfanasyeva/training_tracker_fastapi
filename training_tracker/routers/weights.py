from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from training_tracker.database import database, weights
from training_tracker.models.schemas import User, Weight, WeightIn
from training_tracker.security import get_current_user

router = APIRouter()


@router.post("/weight", response_model=Weight, status_code=201)
async def create_weight(
    weight: WeightIn, current_user: Annotated[User, Depends(get_current_user)]
):
    dict_data = weight.model_dump()
    dict_data["units"] = dict_data["units"].lower()
    existing_data = weights.select().where(
        (weights.c.weight == dict_data["weight"])
        & (weights.c.units == dict_data["units"])
    )
    res = await database.fetch_all(existing_data)
    if res:
        return JSONResponse(
            content={"message": "This weight is already exists"}, status_code=409
        )
    data = {**dict_data, "added_by_user_id": current_user.id}
    query = weights.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/weights", response_model=list[Weight])
async def get_all_weights():
    query = weights.select()
    return await database.fetch_all(query)


@router.get("/weight/{weight_id}", response_model=Weight)
async def get_weight_by_id(weight_id: int):
    query = weights.select().where(weights.c.id == weight_id)
    return await database.fetch_one(query)
