from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class PeopleSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    age: int = Field(...)
    profession: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "age": 25,
                "profession": "Teacher",
            }
        }


class UpdatePeopleModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    age: Optional[int]
    profession: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "age": 25,
                "profession": "Teacher",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}