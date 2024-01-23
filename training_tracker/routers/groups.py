from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from training_tracker.database import database, groups
from training_tracker.models.schemas import Group, GroupIn, User
from training_tracker.security import get_current_user

router = APIRouter()


@router.post("/group", response_model=Group, status_code=201)
async def create_exercise_group(
    group: GroupIn, current_user: Annotated[User, Depends(get_current_user)]
):
    dict_data = group.model_dump()
    existing_data = groups.select().where(groups.c.name == dict_data.get("name"))
    res = await database.fetch_all(existing_data)
    if res:
        return JSONResponse(
            content={"message": "This exercise group is already exists"},
            status_code=403,
        )
    data = {**dict_data, "added_by_user_id": current_user.id}
    query = groups.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/groups", response_model=list[Group])
async def get_all_exercise_groups():
    query = groups.select()
    return await database.fetch_all(query)


@router.get("/group/{group_id}", response_model=Group)
async def get_exercise_group_by_id(group_id: int):
    query = groups.select().where(groups.c.id == group_id)
    return await database.fetch_one(query)
