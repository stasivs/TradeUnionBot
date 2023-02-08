import logging
import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_run import bot
from utils import keyboards, request_funcs
from utils.check_role import super_admin_require
from utils.csv_parser import csv_parser


class RedactStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог редактирования ин-фы о студенте."""
    redact_student_info = State()
    waiting_change_pole = State()
    waiting_new_value = State()
    waiting_confirm = State()


async def redact_student_info(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Отлавливает соответствующий посыл инлайн-кнопки, запускает диалог внесения изменений в бд."""
    logging.info("redact student info button")
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    await RedactStudentInfoFSM.redact_student_info.set()
    async with state.proxy() as data:
        data['bd_id'] = callback_query.data.replace('redact ', '')
    await bot.send_message(callback_query.from_user.id, 'Выберите поле, в которое хотите внести изменения',
                           reply_markup=keyboards.CHANGE_POLE_KEYBOARD)
    await RedactStudentInfoFSM.next()


async def obtain_change_pole(message: types.Message, state: FSMContext) -> None:
    """Отлавливает название поля для последующего изменения, вносит в state.proxy()."""
    async with state.proxy() as data:
        data['pole_name'] = message.text
    await bot.send_message(message.from_user.id, f'Введите новое значение для "{data["pole_name"]}"',
                           reply_markup=keyboards.CANCEL_KEYBOARD)
    await RedactStudentInfoFSM.next()


async def obtain_new_value(message: types.Message, state: FSMContext) -> None:
    """Отлавливает новое значение для ранее выбранного поля, вносит в state.proxy()."""
    async with state.proxy() as data:
        data['new_value'] = message.text
    await bot.send_message(message.from_user.id, f'Внести изменения: {data["pole_name"]} -> {data["new_value"]} ?',
                           reply_markup=keyboards.APPROVAL_KEYBOARD)
    await RedactStudentInfoFSM.next()


async def obtain_confirm(message: types.Message, state: FSMContext) -> None:
    """Отлавливает подтверждение команды об изменении бд, вызывает соответствующую функцию обращения к серверу."""
    if message.text == 'Да':
        async with state.proxy() as data:
            response = await request_funcs.redact_student_info(data['bd_id'], data['pole_name'], data['new_value'])
            if response:
                await bot.send_message(message.from_user.id, 'Изменения внесены',
                                       reply_markup=await keyboards.keyboard_choice(message.from_user.id))
            else:
                await bot.send_message(message.from_user.id, 'Что-то не так, возможно, вы ошиблись при вводе данных',
                                       reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    elif message.text == 'Нет':
        await bot.send_message(message.from_user.id, 'OK',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    await state.finish()


class AddStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог добавления ин-фы о студентах."""
    waiting_csv_file = State()


@super_admin_require
async def add_many_students_info(message: types.Message) -> None:
    """Отлавливает команду '/add_students_data'."""
    await bot.send_message(message.from_user.id, 'Отправьте файл в формате "CSV" с информацией о студентах',
                           reply_markup=keyboards.CANCEL_KEYBOARD)
    await AddStudentInfoFSM.waiting_csv_file.set()


async def get_csv_file(message: types.Message, state: FSMContext) -> None:
    if message.document.file_name.endswith('.csv'):
        await bot.send_message(message.from_user.id, 'Ожидайте...',
                         reply_markup=await keyboards.keyboard_choice(message.from_user.id))
        with await bot.download_file_by_id(message.document.file_id) as file:
            res = await request_funcs.add_many_student_data(await csv_parser(str(file.read(), 'utf-8')))
            if res:
                await bot.send_message(message.from_user.id,
                                       f'Успешно добавлена информация о {res["students_added_counter"]} студентах',
                                       reply_markup=await keyboards.keyboard_choice(message.from_user.id))
            else:
                await bot.send_message(message.from_user.id, 'Не удалось добавить информацию',
                                       reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, 'Неправильный формат файла',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    await state.finish()


def register_super_admin_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(redact_student_info, lambda x: x.data and x.data.startswith('redact '),
                                       state='*')
    dp.register_message_handler(obtain_change_pole,
                                lambda x: x.text in ['Проф карта', 'Студенческий билет', 'Причина мат помощи'],
                                state=RedactStudentInfoFSM.waiting_change_pole)
    dp.register_message_handler(obtain_new_value, content_types=['text'],
                                state=RedactStudentInfoFSM.waiting_new_value)
    dp.register_message_handler(obtain_confirm, lambda x: x.text in ['Да', 'Нет'],
                                state=RedactStudentInfoFSM.waiting_confirm)
    dp.register_message_handler(add_many_students_info, commands=['add_students_data'])
    dp.register_message_handler(get_csv_file, content_types=['document'], state=AddStudentInfoFSM.waiting_csv_file)
