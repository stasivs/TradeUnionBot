
from random import choice
from string import ascii_uppercase
from multiprocessing import Queue
from cryptography.fernet import Fernet
from fastapi import APIRouter, Body
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
queue = []

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
async def get_secret_key():
    key = Fernet.generate_key()
    common_key = Fernet("ENEou4JUwaA0tgBfxUpPgvtOmJW5YQztdwKA4if8vUQ=")
    check_string = "".join(choice(ascii_uppercase) for i in range(12))
    secret_check_string = common_key.encrypt(check_string.encode("utf-8"))
    secret_key = common_key.encrypt(key)
    check_list_queue = {"key": key
                        , "check_string": check_string} 
    check_list_answer = {"secret_key": secret_key
                        , "secret_check_string": secret_check_string} 
                
    queue.append(check_list_queue)
    return ResponseModel(check_list_answer, "Secret key retrieved successfully")

async def check(secret_check_string):
    item = queue.pop()
    key = Fernet(item["key"])
    try:
        check_string = key.decrypt(secret_check_string)
    except:
        return False
    if item["check_string"] == check_string.decode("utf-8"):
        return True
    else:
        return False
