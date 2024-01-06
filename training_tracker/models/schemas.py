import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int | None = None
    email: str
    created_at: datetime.datetime | None = None
    confirmed: bool | None = None


class UserIn(User):
    password: str


class DistanceIn(BaseModel):
    distance: float
    units: str


class Distance(DistanceIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    added_by_user_id: int


class GroupIn(BaseModel):
    name: str


class Group(GroupIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    added_by_user_id: int


class WeightIn(BaseModel):
    weight: float
    units: str


class Weight(WeightIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    added_by_user_id: int


class ExerciseIn(BaseModel):
    name: str
    group_id: int


class Exercise(ExerciseIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    added_by_user_id: int


class Training(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    training_date: datetime.datetime
    status: str
    user_id: int


class SetIn(BaseModel):
    exercise_count: int
    exercise_id: int
    training_id: int
    distance_id: Optional[int] = None
    weight_id: Optional[int] = None


class Set(SetIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    added_by_user_id: int
