from fastapi import APIRouter, Body, status, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from re import compile
import uuid
import asyncio
from cryptography.fernet import Fernet

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
queue = asyncio.Queue(1) # Size of queue. One for processing one query
#COMMON_KEY = os.environ.get("COMMONT_KEY") 

@router.post("/", response_description="Student data added into the database",
             status_code=status.HTTP_201_CREATED,
             response_model=ResponseModel)
async def add_student_data(student: StudentSchema = Body(...)) -> dict:
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return {'data': new_student}


@router.put('/{id}+{token}', response_description="Student data updated",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def update_student_data(id: str, token, student: UpdateStudentSchema = Body(...)) -> dict:
    access = await check(token)    
    if access:
        new_data = {key: val for key, val in student.dict().items() if val}
        if not new_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty data.")
        updated_student = await update_student(id, new_data)
        if not updated_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
        return {'data': updated_student}
    else:
        return ResponseModel("Access denied", "Token is invalid") 


@router.get("/+{token}", response_description="Students retrieved",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def get_students(token) -> dict:
    access = await check(token)    
    if access:
        students = await retrieve_students()
        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Students doesn't exist.")
        return {'data': students}
    else:
        return ResponseModel("Access denied", "Token is invalid") 



@router.get("/by_profcard/{profcard}+{token}", response_description="Student data retrieved",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def get_student_data(profcard: str, token) -> dict:
    access = await check(token)    
    if access:
        if not compile(r'\d{2}-\d{4}').match(profcard):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profcard is not valid.")
        student = await retrieve_student_by_profcard(profcard)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
        return {'data': student}
    else:
        return ResponseModel("Access denied", "Token is invalid") 


@router.get("/by_surname/{surname}+{token}", response_description="Student data retrieved",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def get_student_data(surname: str, token) -> dict:
    access = await check(token)    
    if access:
        student = await retrieve_student_by_surname(surname)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
        return {'data': student}
    else:
        return ResponseModel("Access denied", "Token is invalid")    


@router.get("/by_student_book/{student_book}+{token}", response_description="Student data retrieved",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def get_student_data(student_book: str, token) -> dict:
    access = await check(token)    
    if access:
        if not compile(r'\d{2}-\w-\d{5}').match(student_book):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student_book is not valid.")
        student = await retrieve_student_by_student_book(student_book)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
        return {'data': student}
    else:
        return ResponseModel("Access denied", "Token is invalid")


@router.get("/synchronize", response_description="Secret key for detecting bot")
async def get_secret_key(background_tasks: BackgroundTasks):
    # Background task for detecting unused synchronized links
    background_tasks.add_task(background_check)
    # Common key. Bot also has it
    common_key = Fernet("ENEou4JUwaA0tgBfxUpPgvtOmJW5YQztdwKA4if8vUQ=") # Here is COMMON_KEY 
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

