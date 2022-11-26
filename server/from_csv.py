import asyncio
import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"
# MONGO_DETAILS = "mongodb"


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")


async def add_to_database():
    with open(file='Primer.csv') as file:
        file_data = file
        next(file_data)
        next(file_data)
        for string in file_data:
            data_list = [val if val else None for val in string.replace('\n', '').split(';')]
            await student_collection.insert_one({
                "institute": data_list[0],
                "course": data_list[1],
                "group": data_list[2],
                "surname": data_list[3].split()[0],
                "name": ' '.join(data_list[3].split()[1:]),
                "sex": data_list[4],
                "financing_form": data_list[5],
                "profcard": data_list[6],
                "student_book": data_list[7],
                "role": data_list[8],
                "MP_case": data_list[9],
            })
    return 'Done!'


loop = asyncio.get_event_loop()
tasks = [loop.create_task(add_to_database())]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
