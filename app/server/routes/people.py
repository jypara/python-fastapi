from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

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