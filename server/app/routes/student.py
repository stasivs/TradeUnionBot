from common_key import COMMON_KEY

from fastapi import APIRouter, Body, status, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from re import compile
import uuid
import asyncio
from cryptography.fernet import Fernet
import json

from database import (
    add_student,
    update_student,
    retrieve_students,
    retrieve_student_by_profcard,
    retrieve_student_by_surname,
    retrieve_student_by_student_book,
)
from models.student import (
    ResponseModel,
    StudentSchema,
    UpdateStudentSchema,
)

router = APIRouter()
queue = asyncio.Queue(1)  # Size of queue. One for processing one query


# COMMON_KEY = os.environ.get("COMMONT_KEY")

@router.post("/", response_description="Student data added into the database",
             status_code=status.HTTP_201_CREATED,
             response_model=ResponseModel)
async def add_student_data(student: StudentSchema = Body(...), token: str = None) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="None token.")
    access = await check(token)
    if not access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return {'data': new_student}


@router.put('/{id}', response_description="Student data updated",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def update_student_data(id: str, student: UpdateStudentSchema = Body(...), token: str = None) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="None token.")
    access = await check(token)
    if not access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")
    new_data = {key: val for key, val in student.dict().items() if val}
    if not new_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty data.")
    updated_student = await update_student(id, new_data)
    await encrypt_data(updated_student)
    if not updated_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
    return {'data': updated_student}


@router.get("/", response_description="Students retrieved",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def get_students(token: str = None) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="None token.")
    access = await check(token)
    if not access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")
    students= await retrieve_students()
    encrypt_data(students)
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Students doesn't exist.")
    return {'data': students}


@router.get("/by_profcard/{profcard}", response_description="Student data retrieved",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def get_student_data(profcard: str, token: str = None) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="None token.")
    access = await check(token)
    if not access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")
    if not compile(r'\d{2}-\d{4}').match(profcard):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profcard is not valid.")
    student = await retrieve_student_by_profcard(profcard)
    await encrypt_data(student)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
    return {'data': student}


@router.get("/by_surname/{surname}", response_description="Student data retrieved",
            status_code=status.HTTP_200_OK,
           )
async def get_student_data(surname: str, token: str = None) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="None token.")
    access = await check(token)
    if not access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")
    student = await retrieve_student_by_surname(surname)
    await encrypt_data(student)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
    return {'data': student}


@router.get("/by_student_book/{student_book}", response_description="Student data retrieved",
            status_code=status.HTTP_200_OK,
            )
async def get_student_data(student_book: str, token: str = None) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="None token.")
    access = await check(token)
    if not access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")
    if not compile(r'\d{2}-\w-\d{5}').match(student_book):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student_book is not valid.")
    student = await retrieve_student_by_student_book(student_book)
    await encrypt_data(student)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
    return {'data': student}


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


async def check(url_uuid: str) -> bool:
    try:
        item = queue.get_nowait()
    except:
        return False
    queue.task_done()
    if str(item) == url_uuid:
        return True
    else:
        return False


async def background_check():
    # Life time of unique link
    await asyncio.sleep(0.5)
    if queue.full():
        queue.get_nowait()
        queue.task_done()

async def encrypt_data(data: list[dict]) -> None:
    common_key = Fernet(COMMON_KEY)
    for student in range(len(data)):
        for key in data[student]:
            try:
                data[student][key] = common_key.encrypt(data[student][key].encode("utf-8"))
            except:
                continue
