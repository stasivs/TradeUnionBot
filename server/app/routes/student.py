import uuid
import asyncio
from cryptography.fernet import Fernet
from fastapi import APIRouter, Body, BackgroundTasks
from fastapi.encoders import jsonable_encoder

from database import (
    add_student,
    retrieve_students,
    retrieve_student_by_profcard,
    retrieve_student_by_surname,
    retrieve_student_by_student_book,
)
from models.student import (
    ResponseModel,
    StudentSchema,
    ErrorResponseModel,
)

router = APIRouter()
queue = asyncio.Queue(1) # Size of queue. One for processing one query 

@router.post("/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added successfully.")


@router.get("/+{token}", response_description="Students retrieved")
async def get_students(token):
    access = await check(token)    
    if access:
        #students = await retrieve_students()
        #if students:
        #    return ResponseModel(students, "Students data retrieved successfully")
        #else:
        #    return ResponseModel(students, "Empty list returned")
        return ResponseModel("Access admited", "Success")
    else:
        return ResponseModel("Access denied", "Token is invalid")


@router.get("/by_profcard/{profcard}", response_description="Student data retrieved")
async def get_student_data(profcard):

    student = await retrieve_student_by_profcard(profcard)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")


@router.get("/by_surname/{surname}", response_description="Student data retrieved")
async def get_student_data(surname):
    student = await retrieve_student_by_surname(surname)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")


@router.get("/by_student_book/{student_book}", response_description="Student data retrieved")
async def get_student_data(student_book):
    student = await retrieve_student_by_student_book(student_book)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")


@router.get("/synchronize", response_description="Secret key for detecting bot")
async def get_secret_key(background_tasks: BackgroundTasks):
    # Background task for detecting unused synchronized links
    background_tasks.add_task(background_check)
    # Common key. Bot also has it
    common_key = Fernet("ENEou4JUwaA0tgBfxUpPgvtOmJW5YQztdwKA4if8vUQ=") 
    url_uuid = uuid.uuid4()
    secret_url_uuid = common_key.encrypt(url_uuid.bytes)
    await queue.put(url_uuid)
    return ResponseModel(secret_url_uuid, "Secret key retrieved successfully")

async def check(url_uuid):
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
