from pydantic import BaseModel


class TimetableSchema(BaseModel):
    institute: str
    timetable: str
