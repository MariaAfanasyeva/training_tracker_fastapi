from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from training_tracker.database import (
    database,
    distances,
    exersices,
    sets,
    trainings,
    weights,
)
from training_tracker.models.schemas import Set, SetIn, User
from training_tracker.security import get_current_user

router = APIRouter()


@router.post("/set", response_model=Set, status_code=201)
async def create_set(
    set: SetIn, current_user: Annotated[User, Depends(get_current_user)]
):
    dict_data = set.model_dump()
    # TODO: check how to add validation in pydantic to check that exercise_count > 0
    exercise_id = dict_data.get("exercise_id")
    training_id = dict_data.get("training_id")
    distance_id = dict_data.get("distance_id")
    weight_id = dict_data.get("weight_id")
    if distance_id:
        existing_distance = distances.select().where(distances.c.id == distance_id)
        distance = await database.fetch_one(existing_distance)
        if not distance:
            return JSONResponse(
                content={"message": "Invalid distance id"}, status_code=404
            )
    if weight_id:
        existing_weight = weights.select().where(weights.c.id == weight_id)
        weight = await database.fetch_one(existing_weight)
        if not weight:
            return JSONResponse(
                content={"message": "Invalid weigth id"}, status_code=404
            )
    existing_exercise = exersices.select().where(exersices.c.id == exercise_id)
    exercise = await database.fetch_one(existing_exercise)
    if not exercise:
        return JSONResponse(content={"message": "Invalid exercise id"}, status_code=404)
    existing_training = trainings.select().where(trainings.c.id == training_id)
    training = await database.fetch_one(existing_training)
    if not training:
        return JSONResponse(content={"message": "Invalid training id"}, status_code=404)
    data = {**dict_data, "added_by_user_id": current_user.id}
    query = sets.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/sets", response_model=list[Set])
async def get_all_sets():
    query = sets.select()
    return await database.fetch_all(query)


@router.get("/set/{set_id}", response_model=Set)
async def get_set_by_set_id(set_id: int):
    query = sets.select().where(sets.c.id == set_id)
    return await database.fetch_one(query)
