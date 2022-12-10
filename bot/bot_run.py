from aiogram import Bot
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.utils.request_funcs import get_request_key

from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
request_key = get_request_key()


def start_bot() -> None:
    from bot.handlers.admin import register_admin_handlers
    from bot.handlers.student import register_student_handlers
    from bot.handlers.add_students_data import register_add_students_data_handlers

    register_admin_handlers(dp)
    register_student_handlers(dp)
    register_add_students_data_handlers(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_bot()
