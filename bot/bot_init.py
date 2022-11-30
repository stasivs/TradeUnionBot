from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from request_funcs import get_admin_list
from config import TOKEN


admin_list = get_admin_list()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
