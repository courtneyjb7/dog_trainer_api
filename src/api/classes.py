from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
from pydantic import BaseModel
import sqlalchemy
from datetime import date, time

router = APIRouter()

class class_sort_options(str, Enum):
    type = "type"
    date = "date"

@router.get("/classes/", tags=["classes"])
def get_trainer(
    name: str = "",
    limit: int = Query(50, ge=1, le=250),
    offset: int = Query(0, ge=0),
    sort: class_sort_options = class_sort_options.date
):
    """
    This endpoint returns all the training classes in the database. For every class, it returns:
        `class_id`: the id associated with the class
        `trainer_id`: the id of the trainer teaching the class
        `type`: the type of class
        `date`: the date the class take places
        `num_of_dogs`: the number of dogs attending the class

        You can filter by type or date by using the query parameters `type` or `date`.
    """
    return None

class ClassJson(BaseModel):
    date: date
    start_time: time
    end_time: time
    class_type_id: int


@router.post("/classes/{trainer_id}", tags=["classes"])
def add_classes(trainer_id: int, classes: ClassJson):
    """
    This endpoint adds a new class to a trainer's schedule.
        `date`: the day the class takes place, of datatype DATE
        `start_time`: the time the class starts
        `end_time`: the time the class ends
        `class_type_id`:the id of the type of class
    """
    # verify data types
    # INSERT INTO classes (class_id, trainer_id, date, start_time, end_time, class_type_id) 
            # VALUES (:class_id, :trainer_id, :c2, :movie_id)
    return None

    # TODO: update documentation!