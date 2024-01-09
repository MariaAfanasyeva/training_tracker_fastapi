from typing import Annotated
import sqlachemy
from fastapi import APIRouter, Depends, HTTPException, Request

from training_tracker.database import exersices
from training_tracker.models.schemas import ExerciseIn, Exercise

from training_tracker.models.schemas import User
from training_tracker.security import get_current_user


router = APIRouter()


@router.post("/exercise", response_model=Exercise, status_code=201)
async def create_exercise(exercise: ExerciseIn, 
                          current_user: Annotated[User, Depends(get_current_user)]
                          ):
    pass
