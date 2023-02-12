from pydantic import BaseModel, constr
from typing import Optional, Literal

ProfCard = constr(regex=r"\d{2}-\d{3,4}")
StudentBook = constr(regex=r"\d{2}-\w-\d{5}")


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
    role: Literal["User", "Admin", "SuperAdmin"]
    MP_case: Optional[str]
    telegram_id: Optional[str]


class UpdateStudentSchema(BaseModel):
    institute: Optional[str]
    course: Optional[int]
    group: Optional[str]
    surname: Optional[str]
    name: Optional[str]
    sex: Optional[Literal["муж.", "жен."]]
    financing_form: Optional[Literal["бюджет", "контракт"]]
    profcard: Optional[ProfCard]
    student_book: Optional[StudentBook]
    role: Optional[Literal["User", "Admin", "SuperAdmin"]]
    MP_case: Optional[str]
    telegram_id: Optional[str]


class ResponseStudentSchema(StudentSchema):
    id: str


class ResponseModel(BaseModel):
    data: list[ResponseStudentSchema]


class ManyStudentModel(BaseModel):
    data: list[StudentSchema]


class ResponseManyStudentModel(BaseModel):
    students_added_counter: int
