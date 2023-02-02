import logging

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from utils import check_role

BUTTON_GET_INFO = KeyboardButton('Поиск по базе данных')
BUTTON_PROF_ID = KeyboardButton('Проф карта')
BUTTON_STUD_NUMBER = KeyboardButton('Студенческий билет')
BUTTON_SURNAME = KeyboardButton('Фамилия студента')
BUTTON_FIO = KeyboardButton('ФИО студента')
BUTTON_REASON = KeyboardButton('Причина мат помощи')
BUTTON_YES = KeyboardButton('Да')
BUTTON_NO = KeyboardButton('Нет')

BUTTON_PROFCOME_SCHEDULE = KeyboardButton('Узнать расписание приёма документов')
BUTTON_GET_PROF_ID = KeyboardButton('Узнать номер своей профкарты')
BUTTON_REGISTRATION = KeyboardButton('Регистрация')
BUTTON_IPGS = KeyboardButton('ИПГС')
BUTTON_IAG = KeyboardButton('ИАГ')
BUTTON_IGES = KeyboardButton('ИГЭС')
BUTTON_IIESM = KeyboardButton('ИИЭСМ')
BUTTON_IEUKSN = KeyboardButton('ИЭУКСН')
BUTTON_ICTMS = KeyboardButton('ИЦТМС')
BUTTON_MF = KeyboardButton('МФ')
BUTTON_IFCS = KeyboardButton('ИФКС')
BUTTON_CANCEL = KeyboardButton('Отмена')

ADMIN_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
CHANGE_POLE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
INFO_POLE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
APPROVAL_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)

STUDENT_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
INSTITUTE_NAME_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)

CANCEL_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)

REGISTRATION_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

ADMIN_KEYBOARD.add(BUTTON_GET_INFO)
CHANGE_POLE_KEYBOARD.add(BUTTON_PROF_ID).add(BUTTON_STUD_NUMBER).add(BUTTON_REASON).add(BUTTON_CANCEL)
INFO_POLE_KEYBOARD.add(BUTTON_PROF_ID).add(BUTTON_STUD_NUMBER).add(BUTTON_SURNAME).add(BUTTON_FIO).add(BUTTON_CANCEL)
APPROVAL_KEYBOARD.add(BUTTON_YES).insert(BUTTON_NO)

STUDENT_KEYBOARD.add(BUTTON_PROFCOME_SCHEDULE).add(BUTTON_GET_PROF_ID)
INSTITUTE_NAME_KEYBOARD.add(BUTTON_IPGS).insert(BUTTON_IAG).add(BUTTON_IGES).insert(BUTTON_IIESM) \
    .add(BUTTON_IEUKSN).insert(BUTTON_ICTMS).add(BUTTON_MF).insert(BUTTON_IFCS).add(BUTTON_CANCEL)

CANCEL_KEYBOARD.add(BUTTON_CANCEL)

REGISTRATION_KEYBOARD.add(BUTTON_REGISTRATION)


async def keyboard_choice(user_id: int) -> ReplyKeyboardMarkup:
    if await check_role.is_student_super_admin(user_id):
        logging.warning(f"SuperAdmin is online, id: {user_id}")
        return ADMIN_KEYBOARD
    elif await check_role.is_student_admin(user_id):
        return ADMIN_KEYBOARD
    else:
        return STUDENT_KEYBOARD


async def inline_keyboard_choice(user_id: int, student_bd_id: int) -> InlineKeyboardMarkup:
    redact_keyboard = InlineKeyboardMarkup()
    if await check_role.is_student_super_admin(user_id):
        button_redact = InlineKeyboardButton(text='Редактировать', callback_data=f'redact {student_bd_id}')
        redact_keyboard.add(button_redact)
    else:
        redact_keyboard.add()
    return redact_keyboard
