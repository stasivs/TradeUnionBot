from aiogram import Bot
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN

bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

if __name__ == '__main__':
    from handlers.main import register_main_handlers, register_wtf_handler
    from handlers.admin import register_admin_handlers
    from handlers.student import register_student_handlers
    from handlers.super_admin import register_super_admin_handlers

    register_main_handlers(dp)
    register_super_admin_handlers(dp)
    register_admin_handlers(dp)
    register_student_handlers(dp)
    register_wtf_handler(dp)
    executor.start_polling(dp, skip_updates=True)
