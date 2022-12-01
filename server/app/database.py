import motor.motor_asyncio

# MONGO_DETAILS = "mongodb://localhost:27017"
MONGO_DETAILS = "mongodb"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")


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
    }


# Retrieve all students
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


# Add a new student
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Retrieve a student by profcard
async def retrieve_student_by_profcard(profcard: str) -> list:
    student = await student_collection.find_one({"profcard": profcard})
    if student:
        return [student_helper(student)]


# Retrieve a student by surname
async def retrieve_student_by_surname(surname: str) -> list:
    students = []
    async for student in student_collection.find({"surname": surname}):
        students.append(student_helper(student))
    return students


# Retrieve a student by student_book
async def retrieve_student_by_student_book(student_book: str) -> list:
    student = await student_collection.find_one({"student_book": student_book})
    if student:
        return [student_helper(student)]
