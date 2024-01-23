from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from training_tracker.database import database, exersices
from training_tracker.models.schemas import Exercise, ExerciseIn, User
from training_tracker.security import get_current_user

router = APIRouter()


@router.post("/exercise", response_model=Exercise, status_code=201)
async def create_exercise(
    exercise: ExerciseIn, current_user: Annotated[User, Depends(get_current_user)]
):
    dict_data = exercise.model_dump()
    existing_data = exersices.select().where(
        (exersices.c.name == dict_data.get("name"))
        & (exersices.c.group_id == dict_data.get("group_id"))
    )
    res = await database.fetch_all(existing_data)
    if res:
        return JSONResponse(
            content={"message": "This exercise is already exists"}, status_code=403
        )
    data = {**dict_data, "added_by_user_id": current_user.id}
    query = exersices.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/exercises", response_model=list[Exercise])
async def get_all_exercises():
    query = exersices.select()
    return await database.fetch_all(query)


@router.get("/exercise/{exercises_id}", response_model=Exercise)
async def get_exercises_by_id(exercises_id: int):
    query = exersices.select().where(exersices.c.id == exercises_id)
    return await database.fetch_one(query)
