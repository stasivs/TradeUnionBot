from handlers.main import register_main_handlers, register_wtf_handler
from handlers.admin import register_admin_handlers
from handlers.student import register_student_handlers
from handlers.super_admin import register_super_admin_handlers

from bot_init import dp

if __name__ == 'handlers':
    register_main_handlers(dp)
    register_super_admin_handlers(dp)
    register_admin_handlers(dp)
    register_student_handlers(dp)
    register_wtf_handler(dp)
