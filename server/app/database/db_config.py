import motor.motor_asyncio

# MONGO_DETAILS = "mongodb://localhost:27017"
MONGO_DETAILS = "mongodb"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")
timetable_collection = database.get_collection("timetable_collection")
