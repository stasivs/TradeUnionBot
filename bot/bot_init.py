from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=bot, storage=MemoryStorage())
