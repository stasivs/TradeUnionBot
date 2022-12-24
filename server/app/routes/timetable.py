from fastapi import APIRouter, Body, status, HTTPException
from models.timetable import TimetableSchema
from fastapi.encoders import jsonable_encoder
from database.timetable import (
    retrieve_timetable_by_institute,
    add_timetable,
)

router = APIRouter()


@router.post("/", response_description="Timetable added into the database",
             status_code=status.HTTP_201_CREATED,
             response_model=TimetableSchema)
async def add_student_data(timetable: TimetableSchema = Body(...)) -> dict:
    timetable = jsonable_encoder(timetable)
    new_timetable = await add_timetable(timetable)
    return new_timetable


@router.get("/{institute}", response_description="Timetable retrieved",
            status_code=status.HTTP_200_OK,
            response_model=TimetableSchema)
async def get_timetable_by_institute(institute: str) -> dict:
    timetable = await retrieve_timetable_by_institute(institute)
    if not timetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable doesn't exist.")
    return timetable
