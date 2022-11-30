from aiogram.utils import executor

from admin import register_admin_handlers
from student import register_student_handlers
from request_funcs import get_request_key

from bot_init import dp


if __name__ == '__main__':
    request_key = get_request_key()
    register_admin_handlers(dp)
    register_student_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
