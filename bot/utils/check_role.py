from aiogram import types
from redis import asyncio as aioredis

from utils.request_funcs import get_student_role

redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
# redis = aioredis.from_url("redis://redis", encoding="utf-8", decode_responses=True)


def admin_require(func):
    """Декоратор - проверка на админа"""
    async def wrapper(message: types.Message):
        if await is_student_admin(message.from_user.id):
            await func(message)

    return wrapper


def super_admin_require(func):
    """Декоратор - проверка на суперадмина"""
    async def wrapper(message: types.Message):
        if await is_student_super_admin(message.from_user.id):
            await func(message)

    return wrapper


async def is_student_admin(telegram_id: int) -> bool:
    """Проверяем админ ли студент."""
    role = await redis.get(telegram_id)
    if not role:
        role = get_student_role(telegram_id)
        await redis.set(telegram_id, role, 60 * 60 * 24)
    return True if role == 'Admin' or role == 'SuperAdmin' else False


async def is_student_super_admin(telegram_id: int) -> bool:
    """Проверяем админ ли студент."""
    role = await redis.get(telegram_id)
    if not role:
        role = get_student_role(telegram_id)
        await redis.set(telegram_id, role, 60 * 60 * 24)
    return True if role == 'SuperAdmin' else False
