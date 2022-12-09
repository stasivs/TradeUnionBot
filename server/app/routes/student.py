from fastapi import APIRouter, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from re import compile

from database import (
    add_student,
    update_student,
    retrieve_students,
    retrieve_student_by_profcard,
    retrieve_student_by_surname,
    retrieve_student_by_student_book,
    add_many_student,
    get_role_from_db,
)
from models.student import (
    ResponseModel,
    StudentSchema,
    UpdateStudentSchema,
    ManyStudentModel,
    ResponseManyStudentModel,
)

router = APIRouter()


@router.post("/", response_description="Student data added into the database",
             status_code=status.HTTP_201_CREATED,
             response_model=ResponseModel)
async def add_student_data(student: StudentSchema = Body(...)) -> dict:
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return {'data': new_student}


@router.post("/add_many", response_description="Students data list added into the database",
             status_code=status.HTTP_201_CREATED,
             response_model=ResponseManyStudentModel)
async def add_student_data(students: ManyStudentModel = Body(...)) -> dict:
    students = jsonable_encoder(students)
    result = await add_many_student(students['data'])
    if not result['counter']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data error.")
    return {'students_added_counter': result['counter']}


@router.put('/{id}', response_description="Student data updated",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def update_student_data(id: str, student: UpdateStudentSchema = Body(...)) -> dict:
    new_data = {key: val for key, val in student.dict().items() if val}
    if not new_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty data.")
    updated_student = await update_student(id, new_data)
    if not updated_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
    return {'data': updated_student}


@router.get("/", response_description="Students retrieved",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def get_students() -> dict:
    students = await retrieve_students()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Students doesn't exist.")
    return {'data': students}


@router.get("/by_profcard/{profcard}", response_description="Student data retrieved",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def get_student_data(profcard: str) -> dict:
    if not compile(r'\d{2}-\d{4}').match(profcard):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profcard is not valid.")
    student = await retrieve_student_by_profcard(profcard)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
    return {'data': student}


@router.get("/by_surname/{surname}", response_description="Student data retrieved",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def get_student_data(surname: str) -> dict:
    student = await retrieve_student_by_surname(surname)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
    return {'data': student}


@router.get("/by_student_book/{student_book}", response_description="Student data retrieved",
            status_code=status.HTTP_200_OK,
            response_model=ResponseModel)
async def get_student_data(student_book: str) -> dict:
    if not compile(r'\d{2}-\w-\d{5}').match(student_book):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student_book is not valid.")
    student = await retrieve_student_by_student_book(student_book)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
    return {'data': student}


@router.get('/get_role/{telegram_id}', response_description="Student role retrieved",
            status_code=status.HTTP_200_OK,
            response_model=dict)
async def get_role(telegram_id: str) -> dict:
    student_role = await get_role_from_db(telegram_id)
    if not student_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
    return student_role
