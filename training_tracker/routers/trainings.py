import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from training_tracker.database import database, trainings
from training_tracker.models.schemas import Training, User
from training_tracker.security import get_current_user

router = APIRouter()

def get_current_date():
    return datetime.date.today()

def get_current_user_id(current_user):
    return current_user.id

@router.post("/training", response_model=Training, status_code=201)
async def create_training(current_user: Annotated[User, Depends(get_current_user)]):
    data = {
        "user_id": get_current_user_id(current_user),
        "training_date": get_current_date(),
        "status": "Started",
    }
    query = trainings.insert().values(data)
    last_record_id = await database.execute(query)
    return {
        **data,
        "id": last_record_id,
    }


# TODO: create endpoints for get_trainings_for_user
# training endpoints: get_training_by_id (also awailable only for author), get_training_for_user, get_all_trainings (only for admin)
@router.get("/trainings", response_model=list[Training])
async def get_trainings_for_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    user_id = get_current_user_id(current_user)
    query = trainings.select().where(trainings.c.user_id == user_id)
    return await database.fetch_all(query)


@router.get("/training/{training_id}", response_model=Training)
async def get_training_by_id_for_user(
    current_user: Annotated[User, Depends(get_current_user)], training_id: int
):
    user_id = current_user.id
    query = trainings.select().where(trainings.c.id == training_id)
    training = await database.fetch_one(query)
    if training["user_id"] != user_id:
        return JSONResponse(
            content={"message": "Training with this id doesn't belong you"}, status_code=403
        )
    return training
