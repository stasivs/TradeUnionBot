from fastapi import BackgroundTasks
from fastapi import HTTPException, status
import asyncio
from cryptography.fernet import Fernet
import json
from redis import asyncio as aioredis

redis = aioredis.from_url("redis://localhost:6380", encoding="utf-8", decode_responses=True)


async def verify_token(token: str):
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="None token.")
    access = await check(token)
    if not access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")


async def check(url_uuid: str) -> bool:
    if await redis.getdel(url_uuid) == url_uuid:
        return True
    else:
        return False

