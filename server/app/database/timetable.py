from database.db_config import timetable_collection


def timetable_helper(timetable) -> dict:
    return {
        "id": str(timetable["_id"]),
        "institute": timetable["institute"],
        "timetable": timetable["timetable"],
    }


async def retrieve_timetable_by_institute(institute: str) -> dict:
    timetable = await timetable_collection.find_one({"institute": institute})
    if timetable:
        return timetable_helper(timetable)


async def add_timetable(timetable: dict) -> dict:
    timetable = await timetable_collection.insert_one(timetable)
    new_timetable = await timetable_collection.find_one({"_id": timetable.inserted_id})
    return timetable_helper(new_timetable)
