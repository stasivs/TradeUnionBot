from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

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
    ErrorResponseModel,
)

router = APIRouter()


@router.post("/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added successfully.")


@router.put('/{id}', response_description="Student data updated")
async def update_student_data(id: str, student: UpdateStudentSchema = Body(...)):
    new_data = {key: val for key, val in student.dict().items() if val}
    if not new_data:
        return ErrorResponseModel("An error occurred.", 400, "Empty data.")
    updated_student = await update_student(id, new_data)
    if updated_student:
        return ResponseModel(updated_student, "Student updated successfully.")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")


@router.get("/", response_description="Students retrieved")
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")


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
