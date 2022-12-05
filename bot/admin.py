from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from bot_run import bot, admin_list
import keyboards
import request_funcs


def admin_require(func):
    """Декоратор - проверка на админа"""
    async def wrapper(message: types.Message):
        if message.from_user.id in admin_list:
            await func(message)

    return wrapper


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Выход из машины состояний."""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK', reply_markup=(keyboards.ADMIN_KEYBOARD if message.from_user.id in admin_list
                                            else keyboards.STUDENT_KEYBOARD))


async def greeting(message: types.Message) -> None:
    """Отлавливает команду /start, выводит соответствующую клавиатуру."""
    await bot.send_message(message.from_user.id, "Вас приветствует бот профкома!",
                           reply_markup=(keyboards.ADMIN_KEYBOARD if message.from_user.id in admin_list
                                         else keyboards.STUDENT_KEYBOARD))
    await message.delete()


class GetStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог предоставления ин-фы о студенте."""
    waiting_pole_name = State()
    waiting_value = State()


class RedactStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог редактирования ин-фы о студенте."""
    redact_student_info = State()
    waiting_change_pole = State()
    waiting_new_value = State()
    waiting_confirm = State()


@admin_require
async def get_student_info(message: types.Message) -> None:
    """Отлавливает соответствующий текст кнопки, запускает диалог предоставления ин-фы о студенте."""
    await GetStudentInfoFSM.waiting_pole_name.set()
    await message.reply('Выберите известное вам поле информации о студенте', reply_markup=keyboards.INFO_POLE_KEYBOARD)


async def obtain_pole_name(message: types.Message, state: FSMContext) -> None:
    """Отлавливает название известного поля, вносит в state.proxy()."""
    async with state.proxy() as data:
        data['pole_name'] = message.text
    await GetStudentInfoFSM.next()
    await message.reply(f'Введите значение поля "{data["pole_name"]}"', reply_markup=ReplyKeyboardRemove())


async def obtain_value(message: types.Message, state: FSMContext) -> None:
    """Отлавливает значение известного поля, вносит в state.proxy(),
    вызывает соответствующую функцию обращения к серверу, выводит информацию о студенте."""
    async with state.proxy() as data:
        data['value'] = message.text
        stud_info = await request_funcs.get_student_info(data['pole_name'], data['value'], message)
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
            """, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Редактировать',
                                                                              callback_data=f'redact {student["id"]}')))
        await bot.send_message(message.from_user.id, 'Все пользователи по данному значению поля выведены',
                               reply_markup=keyboards.ADMIN_KEYBOARD)
    else:
        await bot.send_message(message.from_user.id, 'Что-то пошло не так, возможно, вы ошиблись при вводе данных',
                               reply_markup=keyboards.ADMIN_KEYBOARD)
    await state.finish()


async def redact_student_info(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Отлавливает соответствующий посыл инлайн-кнопки, запускает диалог внесения изменений в бд."""
    await RedactStudentInfoFSM.redact_student_info.set()
    async with state.proxy() as data:
        data['id'] = callback_query.data.replace('redact ', '')
    await RedactStudentInfoFSM.next()
    await bot.send_message(callback_query.from_user.id, 'Выберите поле, в которое хотите внести изменения',
                           reply_markup=keyboards.CHANGE_POLE_KEYBOARD)


async def obtain_change_pole(message: types.Message, state: FSMContext) -> None:
    """Отлавливает название поля для последующего изменения, вносит в state.proxy()."""
    async with state.proxy() as data:
        data['pole_name'] = message.text
    await RedactStudentInfoFSM.next()
    await message.reply(f'Введите новое значение для "{data["pole_name"]}"', reply_markup=ReplyKeyboardRemove())


async def obtain_new_value(message: types.Message, state: FSMContext) -> None:
    """Отлавливает новое значение для ранее выбранного поля, вносит в state.proxy()."""
    async with state.proxy() as data:
        data['new_value'] = message.text
    await RedactStudentInfoFSM.next()
    await message.reply(f'Внести изменения: {data["pole_name"]} -> {data["new_value"]} ?',
                        reply_markup=keyboards.APPROVAL_KEYBOARD)


async def obtain_confirm(message: types.Message, state: FSMContext) -> None:
    """Отлавливает подтверждение команды об изменении бд, вызывает соответствующую функцию обращения к серверу."""
    if message.text == 'Да':
        async with state.proxy() as data:
            response = await request_funcs.redact_student_info(data['id'], data['pole_name'], data['new_value'])
            if response:
                await message.reply('Изменения внесены', reply_markup=keyboards.ADMIN_KEYBOARD)
            else:
                await bot.send_message(message.from_user.id, 'Что-то пошло не так, возможно, вы ошиблись при вводе данных',
                               reply_markup=keyboards.ADMIN_KEYBOARD)
    elif message.text == 'Нет':
        await message.reply('OK', reply_markup=keyboards.ADMIN_KEYBOARD)
    await state.finish()


def register_admin_handlers(dp: Dispatcher) -> None:
    """Регистрация админских хендлеров."""
    dp.register_message_handler(cancel_handler, filters.Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(greeting, commands=["start"], state="*")
    dp.register_message_handler(get_student_info, text='Выбрать студента', state=None)
    dp.register_message_handler(obtain_pole_name, content_types=['text'], state=GetStudentInfoFSM.waiting_pole_name)
    dp.register_message_handler(obtain_value, content_types=['text'], state=GetStudentInfoFSM.waiting_value)
    dp.register_callback_query_handler(redact_student_info, lambda x: x.data and x.data.startswith('redact '), state='*')
    dp.register_message_handler(obtain_change_pole, content_types=['text'], state=RedactStudentInfoFSM.waiting_change_pole)
    dp.register_message_handler(obtain_new_value, content_types=['text'], state=RedactStudentInfoFSM.waiting_new_value)
    dp.register_message_handler(obtain_confirm, content_types=['text'], state=RedactStudentInfoFSM.waiting_confirm)
