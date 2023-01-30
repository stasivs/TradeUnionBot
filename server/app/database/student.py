from bson import ObjectId
from bson.errors import InvalidId
from database.db_config import student_collection


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "institute": student["institute"],
        "course": student["course"],
        "group": student["group"],
        "surname": student["surname"],
        "name": student["name"],
        "sex": student["sex"],
        "financing_form": student["financing_form"],
        "profcard": student["profcard"],
        "student_book": student["student_book"],
        "role": student["role"],
        "MP_case": student["MP_case"],
        "telegram_id": student["telegram_id"],
    }


# Retrieve all students
async def retrieve_students() -> list:
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


# Add a new student
async def add_student(student_data: dict) -> list[dict]:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return [student_helper(new_student)]


async def add_many_student(students_data_list: list[dict]) -> dict:
    students = await student_collection.insert_many(students_data_list)
    counter = len(students.inserted_ids)
    return {'counter': counter}


async def update_student(id: str, new_data: dict) -> list[dict]:
    try:
        await student_collection.update_one({"_id": ObjectId(id)}, {"$set": new_data})
        updated_student = await student_collection.find_one({"_id": ObjectId(id)})
        return [student_helper(updated_student)]
    except InvalidId:
        return []


# Retrieve a student by profcard
async def retrieve_student_by_profcard(profcard: str) -> list[dict]:
    student = await student_collection.find_one({"profcard": profcard})
    if student:
        return [student_helper(student)]


# Retrieve a student by surname
async def retrieve_student_by_surname(surname: str) -> list[dict]:
    students = []
    async for student in student_collection.find({"surname": surname}):
        students.append(student_helper(student))
    return students


async def retrieve_student_by_fio(surname: str, name: str) -> list[dict]:
    students = []
    async for student in student_collection.find({"surname": surname, "name": name}):
        students.append(student_helper(student))
    return students


# Retrieve a student by student_book
async def retrieve_student_by_student_book(student_book: str) -> list[dict]:
    student = await student_collection.find_one({"student_book": student_book})
    if student:
        return [student_helper(student)]


async def retrieve_student_by_telegram_id(telegram_id: str) -> list[dict]:
    student = await student_collection.find_one({"telegram_id": telegram_id})
    if student:
        return [student_helper(student)]
