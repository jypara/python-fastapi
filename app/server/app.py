from fastapi import FastAPI, Depends

from server.routes.people import router as PeopleRouter

app = FastAPI()

app.include_router(PeopleRouter, tags=["People"], prefix="/people")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

app.include_router(PeopleRouter, tags=["People"], prefix="/people")
