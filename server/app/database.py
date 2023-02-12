from os import environ

import motor.motor_asyncio

MONGO_URL = environ.get("MONGO_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

database = client.students

student_collection = database.get_collection("students_collection")
timetable_collection = database.get_collection("timetable_collection")
