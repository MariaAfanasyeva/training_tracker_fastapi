from contextlib import asynccontextmanager

from fastapi import FastAPI

from training_tracker.database import database
from training_tracker.routers.distances import router as distances_router
from training_tracker.routers.exercises import router as exercise_router
from training_tracker.routers.groups import router as groups_router
from training_tracker.routers.sets import router as set_router
from training_tracker.routers.trainings import router as training_router
from training_tracker.routers.users import router as user_router
from training_tracker.routers.weights import router as weights_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(groups_router)
app.include_router(weights_router)
app.include_router(distances_router)
app.include_router(exercise_router)
app.include_router(set_router)
app.include_router(training_router)
