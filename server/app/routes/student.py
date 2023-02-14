from .common_key import COMMON_KEY
from .utils import queue, check_wrapper, background_check, check
from fastapi import APIRouter, Body, status, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from re import compile
from cryptography.fernet import Fernet
import uuid
from os import environ

from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder

from services.student import StudentService, get_student_service
from models.student import (
    # ProfCard,
    # StudentBook,
    ResponseModel,
    StudentSchema,
    UpdateStudentSchema,
    ManyStudentModel,
    ResponseManyStudentModel,
)

router = APIRouter()


@router.on_event("startup")
async def init_superadmin():
    student_service = await get_student_service()
    await student_service.add_initial_superadmin(telegram_id=environ.get("SUPERADMIN_TG_ID"))


@router.post(
    path="/",
    response_description="Student data added into the services",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel,
)
async def add_student_data(
        student: StudentSchema = Body(...),
        student_service: StudentService = Depends(get_student_service),
) -> dict:
    student = jsonable_encoder(student)
    return {'data': await student_service.add_student(student_data=student)}


@router.post(
    path="/add_many",
    response_description="Students data list added into the services",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseManyStudentModel,
)
async def add_student_data(
        students: ManyStudentModel = Body(...),
        student_service: StudentService = Depends(get_student_service),
) -> dict:
    students = jsonable_encoder(students)
    return {'students_added_counter': await student_service.add_many_student(students_data_list=students['data'])}


@router.put(
    path='/{student_id}',
    response_description="Student data updated",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
)
async def update_student_data(
        student_id: str,
        student_update: UpdateStudentSchema = Body(...),
        student_service: StudentService = Depends(get_student_service),
) -> dict:
    return {'data': await student_service.update_student(student_id=student_id, student_update=student_update)}


@router.get(
    path="/",
    response_description="Students retrieved",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
)
async def get_students(
        student_service: StudentService = Depends(get_student_service),
) -> dict:
    return {'data': await student_service.get_all_students()}


@router.get(
    path="/by_surname/{surname}",
    response_description="Student data retrieved",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
)
async def get_student_data_by_surname(
        surname: str,
        student_service: StudentService = Depends(get_student_service),
) -> dict:
    return {'data': await student_service.get_student(searching_dict={"surname": surname})}


@router.get(
    path="/by_fio/{fio}",
    response_description="Student data retrieved",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
)
async def get_student_data_by_fio(
        fio: str,
        student_service: StudentService = Depends(get_student_service),
) -> dict:
    return {'data': await student_service.get_student(searching_dict={"fio": fio})}


@router.get(
    path="/by_profcard/{profcard}",
    response_description="Student data retrieved",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
)
async def get_student_data_by_profcard(
        # profcard: ProfCard,
        profcard: str,
        student_service: StudentService = Depends(get_student_service),
) -> dict:
    return {'data': await student_service.get_student(searching_dict={"profcard": str(profcard)})}


@router.get(
    path="/by_student_book/{student_book}",
    response_description="Student data retrieved",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
)
async def get_student_data_by_student_book(
        # student_book: StudentBook,
        student_book: str,
        student_service: StudentService = Depends(get_student_service),
) -> dict:
    return {'data': await student_service.get_student(searching_dict={"student_book": student_book})}


@router.get(
    path='/by_telegram_id/{telegram_id}',
    response_description="Student role retrieved",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
)
async def get_student_data_by_telegram_id(
        telegram_id: str,
        student_service: StudentService = Depends(get_student_service),
) -> dict:
    return {'data': await student_service.get_student(searching_dict={"telegram_id": telegram_id})}


@router.delete(
    path='/{student_id}',
    response_description="Student data updated",
    status_code=status.HTTP_200_OK,
    response_model=dict,
)
async def delete_student(
        student_id: str,
        student_service: StudentService = Depends(get_student_service),
) -> dict:
    return {'data': await student_service.delete_student(student_id=student_id)}


@router.get("/synchronize", response_description="Secret key for detecting bot")
async def get_secret_key(background_tasks: BackgroundTasks):
    # Common key. Bot also has it
    common_key = Fernet(COMMON_KEY)  # Here is COMMON_KEY
    url_uuid = uuid.uuid4()
    secret_url_uuid = common_key.encrypt(url_uuid.bytes)
    await queue.put(url_uuid) 
    # Background task for detecting unused synchronized links
    background_tasks.add_task(background_check)
    return {'data': secret_url_uuid}
