from fastapi import FastAPI
from training_tracker.database import database
from training_tracker.routers.users import router as user_router
from training_tracker.routers.groups import router as groups_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(user_router)
app.include_router(groups_router)

@app.get("/")
async def hello():
    return {"message": "Hello, world!"}
