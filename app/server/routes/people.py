from fastapi import APIRouter, Body, Request, Response, status
from starlette.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
import json, base64

from server import database as ww
from server.models.people import *

from server.database import (
    add_people,
    delete_people,
    retrieve_person,
    retrieve_people,
    update_people,
)
from server.models.people import (
    ErrorResponseModel,
    ResponseModel,
    PeopleSchema,
    UpdatePeopleModel,
)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates/")


@router.get("/", response_description="peoples retrieved")
async def get_peoples(request: Request):
    peoples = await retrieve_people()
    return templates.TemplateResponse('index.html', context={'request': request, 'people': peoples}) \
        if len(peoples) > 0 \
        else ResponseModel(
        peoples, "Empty list returned")


@router.get("/{id}", response_description="people data retrieved")
async def get_people_data(request: Request, id):
    people = await retrieve_person(id)
    # route =
    return templates.TemplateResponse('edit.form.html', context={'request': request, 'people': people}) \
        if len(people) > 0 \
        else ResponseModel(
        people, "Empty list returned")


@router.post("/", response_description="people data added into the database")
async def add_people_data(people: PeopleSchema = Body(...)):
    people = jsonable_encoder(people)
    new_people = await add_people(people)
    return ResponseModel(new_people, "people added successfully.")


@router.delete("/{id}", response_description="people data deleted from the database")
async def delete_people_data(id: str):
    deleted_people = await delete_people(id)
    return ResponseModel("people with ID: {} removed".format(id), "people deleted successfully") \
        if deleted_people \
        else ErrorResponseModel("An error occured", 404, "people with id {0} doesn't exist".format(id))


@router.put("/{id}", response_class=Response)
async def update_people_data(request: Request,id, req: UpdatePeopleModel = Body(...)):
    print(base64.b64decode(req))
    # data = json.dumps(req).format()
    updated_student = update_people(id, req)
    if updated_student:
        return ResponseModel("people with ID removed people deleted successfully","hello")
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )
    # return templates.TemplateResponse('index.html', context={'request': request})

    # updated_people = await update_people(id, req.dict())
    # return templates.TemplateResponse('index.html', context={'request': request})