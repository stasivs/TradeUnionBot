from fastapi import FastAPI
from routes.student import router as StudentRouter
from routes.timetable import router as TimetableRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")
app.include_router(TimetableRouter, tags=['Timetable'], prefix="/timetable")
