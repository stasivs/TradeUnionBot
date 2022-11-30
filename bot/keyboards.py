from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


BUTTON_MAT_HELP = KeyboardButton('Редактировать информацию о студенте')
BUTTON_GET_INFO = KeyboardButton('Уточнить информацию о студенте')
BUTTON_PROF_ID = KeyboardButton('Проф карта')
BUTTON_STUD_NUMBER = KeyboardButton('Студенческий билет')
BUTTON_SURNAME = KeyboardButton('Фамилия студента')
BUTTON_REASON = KeyboardButton('Причина мат помощи')
BUTTON_YES = KeyboardButton('Да')
BUTTON_NO = KeyboardButton('Нет')

BUTTON_GET_SCHEDULE = KeyboardButton('Узнать расписание профкома')
BUTTON_GET_PROF_ID = KeyboardButton('Узнать номер своей профкарты')
BUTTON_REGISTRATION = KeyboardButton('Пройти регистрацию')


ADMIN_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
CHANGE_POLE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
INFO_POLE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
APPROVAL_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)

STUDENT_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)


ADMIN_KEYBOARD.add(BUTTON_MAT_HELP).add(BUTTON_GET_INFO).add(BUTTON_GET_SCHEDULE).add(BUTTON_GET_PROF_ID).add(BUTTON_REGISTRATION)
CHANGE_POLE_KEYBOARD.add(BUTTON_PROF_ID).add(BUTTON_STUD_NUMBER).add(BUTTON_REASON)
INFO_POLE_KEYBOARD.add(BUTTON_PROF_ID).add(BUTTON_STUD_NUMBER).add(BUTTON_SURNAME)
APPROVAL_KEYBOARD.add(BUTTON_YES).add(BUTTON_NO)

STUDENT_KEYBOARD.add(BUTTON_GET_SCHEDULE).add(BUTTON_GET_PROF_ID).add(BUTTON_REGISTRATION)
