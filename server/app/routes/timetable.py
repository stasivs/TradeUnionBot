from fastapi import APIRouter, Body, status, HTTPException, Depends
from models.timetable import TimetableSchema
from fastapi.encoders import jsonable_encoder
from services.timetable import TimetableService, get_timetable_service
from services.encryption import verify_token, queue, background_check

router = APIRouter()


@router.post(
    path="/",
    response_description="Timetable added into the services",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_token),],
    response_model=TimetableSchema,
)
async def add_student_data(
        timetable: TimetableSchema = Body(...),
        timetable_service: TimetableService = Depends(get_timetable_service),
) -> dict:
    timetable = jsonable_encoder(timetable)
    return await timetable_service.add_timetable(timetable=timetable)


@router.get(
    path="/{institute}",
    response_description="Timetable retrieved",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_token),],
    response_model=TimetableSchema,
)
async def get_timetable_by_institute(
        institute: str,
        timetable_service: TimetableService = Depends(get_timetable_service),
) -> dict:
    return await timetable_service.get_timetable(institute=institute)
