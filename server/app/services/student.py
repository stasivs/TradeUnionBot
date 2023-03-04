from bson import ObjectId
from bson.errors import InvalidId
from database import student_collection
from fastapi import status, HTTPException

from models.student import UpdateStudentSchema


class StudentService:
    @staticmethod
    def student_helper(student) -> dict:
        return {
            "id": str(student["_id"]),
            "institute": student["institute"],
            "course": student["course"],
            "group": student["group"],
            "surname": student["surname"],
            "name": student["name"],
            "birthdate": student["birthdate"],
            "sex": student["sex"],
            "financing_form": student["financing_form"],
            "profcard": student["profcard"],
            "student_book": student["student_book"],
            "role": student["role"],
            "MP_case": student["MP_case"],
            "comment": student["comment"],
            "telegram_id": student["telegram_id"],
        }

    async def get_all_students(self) -> list:
        students = []
        async for student in student_collection.find():
            students.append(self.student_helper(student))
        return students

    async def add_student(self, student_data: dict) -> list[dict]:
        student = await student_collection.insert_one(student_data)
        new_student = await student_collection.find_one({"_id": student.inserted_id})
        return [self.student_helper(new_student)]

    async def add_many_student(self, students_data_list: list[dict]) -> int:
        students = await student_collection.insert_many(students_data_list)
        counter = len(students.inserted_ids)
        if not counter:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data error.")
        return counter

    async def update_student(self, student_id: str, student_update: UpdateStudentSchema) -> list[dict]:
        new_data = {key: val for key, val in student_update.dict().items() if val}
        if not new_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty data.")
        try:
            await student_collection.update_one({"_id": ObjectId(student_id)}, {"$set": new_data})
            updated_student = await student_collection.find_one({"_id": ObjectId(student_id)})
            return [self.student_helper(updated_student)]
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")

    async def get_student(self, searching_dict: dict) -> list[dict]:
        if "fio" in searching_dict:
            surname, *name = searching_dict["fio"].split()
            searching_dict = {"surname": surname, "name": " ".join(name)}
        students = []
        async for student in student_collection.find(searching_dict):
            students.append(self.student_helper(student))
        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")
        return students

    async def delete_student(self, student_id: str) -> str:
        try:
            await student_collection.delete_one({"_id": ObjectId(student_id)})
            return "Deleted successful"
        except InvalidId:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student doesn't exist.")

    # async def add_initial_superadmin(self, telegram_id: str) -> None:
    #     try:
    #         await self.get_student(searching_dict={"surname": "SuperAdmin"})
    #     except HTTPException:
    #         await self.add_student(student_data={
    #             "institute": "SuperAdmin",
    #             "course": 999,
    #             "group": "SuperAdmin",
    #             "surname": "SuperAdmin",
    #             "name": "SuperAdmin",
    #             "sex": "муж.",
    #             "financing_form": "бюджет",
    #             "profcard": None,
    #             "student_book": None,
    #             "role": "SuperAdmin",
    #             "MP_case": "SuperAdmin",
    #             "telegram_id": telegram_id,
    #         })


async def get_student_service() -> StudentService:
    return StudentService()
