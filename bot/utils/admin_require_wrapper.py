from aiogram import types
from bot.utils.request_funcs import is_student_admin


def admin_require(func):
    """Декоратор - проверка на админа"""

    async def wrapper(message: types.Message):
        if await is_student_admin(message.from_user.id):
            await func(message)

    return wrapper
