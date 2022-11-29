from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_mat_help = KeyboardButton('Редактировать информацию о студенте')
button_get_info = KeyboardButton('Уточнить информацию о студенте')
button_prof_id = KeyboardButton('Проф карта')
button_stud_number = KeyboardButton('Студенческий билет')
button_surname = KeyboardButton('Фамилия студента')
button_reason = KeyboardButton('Причина мат помощи')
button_yes = KeyboardButton('Да')
button_no = KeyboardButton('Нет')

button_get_schedule = KeyboardButton('Узнать расписание профкома')
button_get_prof_id = KeyboardButton('Узнать номер своей профкарты')
button_registration = KeyboardButton('Пройти регистрацию')


admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
change_pole_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
info_pole_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
approval_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

student_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)


admin_keyboard.add(button_mat_help).add(button_get_info).add(button_get_schedule).add(button_get_prof_id).add(button_registration)
change_pole_keyboard.add(button_prof_id).add(button_stud_number).add(button_reason)
info_pole_keyboard.add(button_prof_id).add(button_stud_number).add(button_surname)
approval_keyboard.add(button_yes).add(button_no)

student_keyboard.add(button_get_schedule).add(button_get_prof_id).add(button_registration)
