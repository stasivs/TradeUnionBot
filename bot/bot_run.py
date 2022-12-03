from aiogram import Bot
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from request_funcs import get_request_key

from request_funcs import get_admin_list
from config import TOKEN

admin_list = get_admin_list()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
request_key = get_request_key()


def start_bot() -> None:
    from admin import register_admin_handlers
    from student import register_student_handlers

    register_admin_handlers(dp)
    register_student_handlers(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    start_bot()
