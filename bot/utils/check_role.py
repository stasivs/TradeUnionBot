from aiogram import types
from redis import asyncio as aioredis

from utils.request_funcs import get_student_info
from config import EXPIRE_VALUE

# redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)


redis = aioredis.from_url("redis://redis", encoding="utf-8", decode_responses=True)


def admin_require(func):
    """Декоратор - проверка на админа"""

    async def wrapper(message: types.Message):
        if await check_student_role(message.from_user.id) in ['Admin', 'SuperAdmin']:
            await func(message)

    return wrapper


def super_admin_require(func):
    """Декоратор - проверка на суперадмина"""

    async def wrapper(message: types.Message, state=None):
        if await check_student_role(message.from_user.id) == 'SuperAdmin':
            if state:
                await func(message, state)
            else:
                await func(message)

    return wrapper


async def check_student_role(telegram_id: int) -> str:
    """
    Проверка на роль через redis, если не находит там, обращается к монго, если не находит там,
    выбирает 'NotFound', конечный вариант выдаёт.
    """
    role = await redis.get(telegram_id)

    if not role:
        stud_info = await get_student_info('Телеграм ID', telegram_id)
        if isinstance(stud_info, list):
            role = stud_info[0]['role']
        else:
            return 'NotFound'
        await redis.set(telegram_id, role, EXPIRE_VALUE)
    return role
