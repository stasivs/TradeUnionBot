from re import compile
from pydantic import BaseModel, validator
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
    token: str

    @validator('profcard')
    def prfcard_validator(cls, value):
        if not compile(r'\d{2}-\d{4}').match(value):
            raise ValueError('Profcard is not valid')
        return value

    @validator('student_book')
    def student_book_validator(cls, value):
        if not compile(r'\d{2}-\w-\d{5}').match(value):
            raise ValueError('Student_book is not valid')
        return value


class UpdateStudentSchema(StudentSchema):
    institute: Optional[str]
    course: Optional[int]
    group: Optional[str]
    surname: Optional[str]
    name: Optional[str]
    sex: Optional[Literal["муж.", "жен."]]
    financing_form: Optional[Literal["бюджет", "контракт"]]
    role: Optional[Literal["User", "Admin"]]


class ResponseStudentSchema(StudentSchema):
    id: str


class ResponseModel(BaseModel):
    data: list[ResponseStudentSchema]
