from fastapi import FastAPI

from training_tracker.database import database
from training_tracker.routers.distances import router as distances_router
from training_tracker.routers.groups import router as groups_router
from training_tracker.routers.users import router as user_router
from training_tracker.routers.weights import router as weights_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(user_router)
app.include_router(groups_router)
app.include_router(weights_router)
app.include_router(distances_router)
