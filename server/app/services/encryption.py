from common_key import COMMON_KEY
from fastapi import BackgroundTasks
from fastapi import HTTPException, status
import asyncio
from cryptography.fernet import Fernet
import json
from functools import wraps

queue = asyncio.Queue(1)  # Size of queue. One for processing one query

async def verify_token(token: str):
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="None token.")
    access = await check(token)
    if not access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")


async def check(url_uuid: str) -> bool:
    try:
        item = queue.get_nowait()
    except:
        return False
    queue.task_done()
    if str(item) == url_uuid:
        return True
    else:
        return False


async def background_check():
    # Life time of unique link
    await asyncio.sleep(0.5)
    if queue.full():
        queue.get_nowait()
        queue.task_done()


async def encrypt_data(data: list[dict]) -> None:
    common_key = Fernet(COMMON_KEY)
    for student in range(len(data)):
        for key in data[student]:
            try:
                data[student][key] = common_key.encrypt(data[student][key].encode("utf-8"))
            except:
                continue
