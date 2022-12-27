import logging
import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_run import bot
from utils import keyboards, request_funcs
from utils.check_role import admin_require


class GetStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог предоставления ин-фы о студенте."""
    waiting_pole_name = State()
    waiting_value = State()


@admin_require
async def get_student_info(message: types.Message) -> None:
    """Отлавливает соответствующий текст кнопки, запускает диалог предоставления ин-фы о студенте."""
    logging.info("choose student button")
    await message.reply('Выберите известное вам поле информации о студенте', reply_markup=keyboards.INFO_POLE_KEYBOARD)
    await GetStudentInfoFSM.waiting_pole_name.set()


async def obtain_pole_name(message: types.Message, state: FSMContext) -> None:
    """Отлавливает название известного поля, вносит в state.proxy()."""
    async with state.proxy() as data:
        data['pole_name'] = message.text
    await message.reply(f'Введите значение поля "{data["pole_name"]}"', reply_markup=keyboards.CANCEL_KEYBOARD)
    await GetStudentInfoFSM.next()


async def obtain_value(message: types.Message, state: FSMContext) -> None:
    """
    Отлавливает значение известного поля, вносит в state.proxy(),
    вызывает соответствующую функцию обращения к серверу, выводит информацию о студенте,
    выдаёт инлайн кнопку для суперадмина
    """
    logging.info(f"stud info got: {message.text}")
    async with state.proxy() as data:
        data['value'] = message.text
        stud_info = await request_funcs.get_student_info(data['pole_name'], data['value'])
    if stud_info:
        for student in stud_info:
            await bot.send_message(message.from_user.id, f"""
                Институт: {student['institute']}
Курс: {student['course']}
Группа: {student['group']}
Фамилия: {student['surname']}
Имя: {student['name']}
Пол: {student['sex']}
Форма финансирования: {student['financing_form']}
Номер профкарты: {student['profcard']}
Номер студенческого билета: {student['student_book']}
Причина получения МП: {student['MP_case']}
            """, reply_markup=await keyboards.inline_keyboard_choice(message.from_user.id, student["id"]))
        await bot.send_message(message.from_user.id, 'Пользователи выведены',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, 'Что-то не так, возможно, вы ошиблись при вводе данных',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    await state.finish()


def register_admin_handlers(dp: Dispatcher) -> None:
    """Регистрация админских хендлеров."""
    dp.register_message_handler(get_student_info, text='Выбрать студента', state=None)
    dp.register_message_handler(obtain_pole_name,
                                lambda x: x.text in ['Проф карта', 'Студенческий билет', 'Фамилия студента', 'ФИО студента'],
                                state=GetStudentInfoFSM.waiting_pole_name)
    dp.register_message_handler(obtain_value, lambda x: any(re.search(i, x.text, flags=0) for i in
                                                            [r'\b\d{2}-\d{4}\b', r'\b\d{2}-[А-Я]-\d{5}\b',
                                                             r'\b[А-Я]{1}[а-яё]{1,20}\b',
                                                             r'[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+']),
                                state=GetStudentInfoFSM.waiting_value)
