from aiogram import types
from redis import asyncio as aioredis

from utils.request_funcs import get_student_info
from config import EXPIRE_VALUE

redis = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)


#redis = aioredis.from_url("redis://redis", encoding="utf-8", decode_responses=True)


def admin_require(func):
    """Декоратор - проверка на админа"""

    async def wrapper(message: types.Message):
        if True:#await is_student_admin(message.from_user.id):
            await func(message)

    return wrapper


def super_admin_require(func):
    """Декоратор - проверка на суперадмина"""

    async def wrapper(message: types.Message, state=None):
        if await is_student_super_admin(message.from_user.id):
            if state:
                await func(message, state)
            else:
                await func(message)

    return wrapper


async def is_student_admin(telegram_id: int) -> bool:
    """
    Проверка на админа через redis, если не находит там, обращается к монго, если не находит там,
    выбирает User, конечный вариант заносит в redis, выдаёт bool результат.
    """
    role = await redis.get(telegram_id)

    if not role:
        stud_info = await get_student_info('telegram_id', telegram_id)
        if stud_info:
            role = stud_info[0]['role']
        else:
            role = 'User'
        await redis.set(telegram_id, role, EXPIRE_VALUE)
    return True if role == 'Admin' or role == 'SuperAdmin' else False


async def is_student_super_admin(telegram_id: int) -> bool:
    """
    Проверка на суперадмина через redis, если не находит там, обращается к монго, если не находит там,
    выбирает User, конечный вариант заносит в redis, выдаёт bool результат.
    """
    role = await redis.get(telegram_id)

    if not role:
        stud_info = await get_student_info('telegram_id', telegram_id)
        if stud_info:
            role = stud_info[0]['role']
        else:
            role = 'User'
        await redis.set(telegram_id, role, EXPIRE_VALUE)
    return True if role == 'SuperAdmin' else False
