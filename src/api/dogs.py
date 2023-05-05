from fastapi import APIRouter, HTTPException
from enum import Enum
from src import database as db
from fastapi.params import Query
import sqlalchemy

router = APIRouter()


@router.get("/dogs/{dog_id}", tags=["dogs"])
def get_dog(dog_id: int):
    """
    This endpoint returns information about a dog in the database. For every dog, it returns:
        `dog_id`: the id associated with the dog
        `name`: the name of the dog
        `client_email`: the email of the owner of the dog
        `birthday`: the dog’s date of birth
        `breed`: the dog’s breed
        `trainer_comments`: a string of comments from the trainer about the dog’s progress (optional)
    """
    stmt = sqlalchemy.text("""                            
            SELECT *
            FROM dogs
            WHERE dogs.dog_id = (:id)                        
        """)

    with db.engine.connect() as conn:
        result = conn.execute(stmt, [{"id": dog_id}])
        json = []
        for row in result:
            json.append(
                {
                    "dog_id": row.dog_id,
                    "name": row.dog_name,
                    "client_email": row.client_email, 
                    "birthday": row.birthday,
                    "breed": row.breed
                }
            )
    if json != []:
        return json
    
    raise HTTPException(status_code=404, detail="trainer not found.")

@router.get("/dogs/{dog_id}", tags=["dogs"])
def get_dog(dog_id: int):
    """
    This endpoint returns information about a dog in the database. For every dog, it returns:
        `dog_id`: the id associated with the dog
        `name`: the name of the dog
        `client_email`: the email of the owner of the dog
        `birthday`: the dog's date of birth
        `breed`: the dog's breed
        `trainer_comments`: a list of comments from the trainer about the dog's progress (optional)

            Each comment returns:
                `comment_id`: the id of the comment
                `trainer`: the name of the trainer who wrote the comment
                `time_added`: the day and time the comment was made
                `text`: the comment text

    """
    stmt = sqlalchemy.text("""                            
        SELECT *
        FROM dogs
        LEFT JOIN comments on comments.dog_id = dogs.dog_id
        LEFT JOIN trainers on comments.trainer_id = trainers.trainer_id
        WHERE dogs.dog_id = :id
        ORDER BY comments.time_added desc
    """)

    with db.engine.connect() as conn:
        result = conn.execute(stmt, [{"id": dog_id}])
        table = result.fetchall()
        if table == []:
            raise HTTPException(status_code=404, detail="dog not found.")
        row1 = table[0]
        json = {
            "dog_id": row1.dog_id,
            "name": row1.dog_name,
            "client_email": row1.client_email, 
            "birthday": row1.birthday,
            "breed": row1.breed,
            "trainer_comments": []
        }
        if row1.comment_id is not None:
            for row in table:
                json["dogs_attended"].append(
                    {
                        "comment_id": row.comment_id,
                        "trainer": row.first_name + " " + row.last_name,
                        "time_added": row.time_added,
                        "text": row.comment_text
                    }
                )
    
    return json