from pydantic import BaseModel
from typing import Optional, Literal


class StudentSchema(BaseModel):
    institute: str
    course: int
    group: str
    surname: str
    name: str
    sex: Literal["муж.", "жен."]
    financing_form: Literal["бюджет", "контракт"]
    profcard: Optional[str]
    student_book: Optional[str]
    role: Literal["User", "Admin"]
    MP_case: Optional[str]


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
