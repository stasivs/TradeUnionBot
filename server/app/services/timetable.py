from fastapi import status, HTTPException

from database import timetable_collection


class TimetableService:
    @staticmethod
    def timetable_helper(timetable) -> dict:
        return {
            "id": str(timetable["_id"]),
            "institute": timetable["institute"],
            "timetable": timetable["timetable"],
        }

    async def get_all_timetables(self) -> list:
        timetables = []
        async for timetable in timetable_collection.find():
            timetables.append(self.timetable_helper(timetable))
        return timetables

    async def get_timetable(self, institute: str) -> dict:
        timetable = await timetable_collection.find_one({"institute": institute})
        if not timetable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable doesn't exist.")
        return self.timetable_helper(timetable)

    async def add_timetable(self, timetable: dict) -> dict:
        old_timetable = await timetable_collection.find_one({"institute": timetable["institute"]})
        if old_timetable:
            await timetable_collection.update_one({"_id": old_timetable["_id"]}, {"$set": timetable})
            timetable_id = old_timetable["_id"]
        else:
            timetable = await timetable_collection.insert_one(timetable)
            timetable_id = timetable.inserted_id
        new_timetable = await timetable_collection.find_one({"_id": timetable_id})
        return self.timetable_helper(new_timetable)


async def get_timetable_service() -> TimetableService:
    return TimetableService()
