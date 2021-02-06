from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://testUser:pass123@cluster0.splhr.mongodb.net/testDB?retryWrites=true&w=majority")

db = client['testDB']
people_collection = db['people']


class People(BaseModel):
    _id: int
    fullname: str
    email: str
    age: int
    profession: str



class Person(People):
    id: int


class PersonUpdate(People):
    fullname: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    profession: Optional[str] = None


def people_helper(people) -> dict:
    return {
        "id": str(people["_id"]),
        "fullname": people["fullname"],
        "email": people["email"],
        "age": people["age"],
        "profession": people["profession"],
    }


async def retrieve_people():
    peoples = []
    async for people in people_collection.find():
        peoples.append(people_helper(people))
    return peoples


# Add a new people into to the database
async def add_people(people_data: dict) -> dict:
    people = await people_collection.insert_one(people_data)
    new_people = await people_collection.find_one({"_id": people.inserted_id})
    return people_helper(new_people)


# Retrieve a people with a matching ID
async def retrieve_person(id: str) -> dict:
    people = await people_collection.find_one({"_id": ObjectId(id)})
    if people:
        return people_helper(people)


# Update a people with a matching ID
async def update_people(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    people = await people_collection.find_one({"_id": ObjectId(id)})
    if people:
        updated_people = await people_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_people:
            return True
        return False


# Delete a people from the database
async def delete_people(id: str):
    people = await people_collection.find_one({"_id": ObjectId(id)})
    if people:
        await people_collection.delete_one({"_id": ObjectId(id)})
        return True