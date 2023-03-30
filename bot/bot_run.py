from aiogram.utils import executor

from bot_init import dp
import middlewares
import handlers

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
