from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from bot_init import bot, admin_list
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
    await message.reply('OK', reply_markup=(keyboards.admin_keyboard if message.from_user.id in admin_list else keyboards.student_keyboard))


async def greeting(message: types.Message) -> None:
    """Отлавливает команду /start, выводит соответствующую клавиатуру."""
    await bot.send_message(message.from_user.id, "Вас приветствует бот профкома!", reply_markup=(keyboards.admin_keyboard if message.from_user.id in admin_list else keyboards.student_keyboard))
    await message.delete()


@admin_require
async def make_record(message: types.Message) -> None:
    """Отлавливает соответствующий текст кнопки, запускает диалог внесения изменений в бд."""
    await MakeRecordFSM.waiting_prof_id.set()
    await message.reply('Введите номер профкарты студента', reply_markup=ReplyKeyboardRemove())


@admin_require
async def get_student_info(message: types.Message) -> None:
    """Отлавливает соответствующий текст кнопки, запускает диалог предоставления ин-фы о студенте."""
    await GetStudentInfoFSM.waiting_pole_name.set()
    await message.reply('Выберите известное вам поле информации о студенте', reply_markup=keyboards.info_pole_keyboard)


class MakeRecordFSM(StatesGroup):
    """Машина состояний - диалог внесения изменений в бд."""
    waiting_prof_id = State()
    waiting_change_pole = State()
    waiting_new_value = State()
    waiting_confirm = State()


async def obtain_prof_id(message: types.Message, state: FSMContext) -> None:
    """Отлавливает номер профкарты при запущенном диалоге MakeRecordFSM, вносит в state.proxy()."""
    async with state.proxy() as data:
        data['prof_id'] = message.text
    await MakeRecordFSM.next()
    await message.reply('Выберите поле, в которое хотите внести изменения', reply_markup=keyboards.change_pole_keyboard)


async def obtain_change_pole(message: types.Message, state: FSMContext) -> None:
    """Отлавливает название поля для последующего изменения, вносит в state.proxy()."""
    async with state.proxy() as data:
        data['pole_name'] = message.text
    await MakeRecordFSM.next()
    await message.reply(f'Введите новое значение для {data["pole_name"]}', reply_markup=ReplyKeyboardRemove())


async def obtain_new_value(message: types.Message, state: FSMContext) -> None:
    """Отлавливает новое значение для ранее выбранного поля, вносит в state.proxy()."""
    async with state.proxy() as data:
        data['new_value'] = message.text
    await MakeRecordFSM.next()
    await message.reply(f'Внести изменения: {data["pole_name"]} -> {data["new_value"]} ?',
                        reply_markup=keyboards.approval_keyboard)


async def obtain_confirm(message: types.Message, state: FSMContext) -> None:
    """Отлавливает подтверждение команды об изменении бд, вызывает соответствующую функцию обращения к серверу."""
    if message.text == 'Да':
        async with state.proxy() as data:
            await request_funcs.redact_student_info(data['prof_id'], data['pole_name'], data['new_value'])
            await message.reply('Изменения внесены', reply_markup=keyboards.admin_keyboard)
    elif message.text == 'Нет':
        await message.reply('OK', reply_markup=keyboards.admin_keyboard)
    await state.finish()


class GetStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог предоставления ин-фы о студенте."""
    waiting_pole_name = State()
    waiting_value = State()


async def obtain_pole_name(message: types.Message, state: FSMContext) -> None:
    """Отлавливает название известного поля, вносит в state.proxy()."""
    async with state.proxy() as data:
        data['pole_name'] = message.text
    await GetStudentInfoFSM.next()
    await message.reply(f'Введите значение поля {data["pole_name"]}', reply_markup=ReplyKeyboardRemove())


async def obtain_value(message: types.Message, state: FSMContext) -> None:
    """Отлавливает значение известного поля, вносит в state.proxy(),
    вызывает соответствующую функцию обращения к серверу, выводит информацию о студенте."""
    async with state.proxy() as data:
        data['value'] = message.text
        stud_info = await request_funcs.get_student_info(data['pole_name'], data['value'])
    await message.reply(f"""
        Институт: {stud_info['inst']}
Курс: {stud_info['curs']}
Группа: {stud_info['group']}
ФИО: {stud_info['fio']}
Пол: {stud_info['sex']}
Форма финансирования: {stud_info['financing']}
Номер профкарты: {stud_info['prof_id']}
Номер студенческого билета: {stud_info['stud_id']}
Причина получения МП: {stud_info['reason']}
    """, reply_markup=keyboards.admin_keyboard)
    await state.finish()


def register_admin_handlers(dp: Dispatcher):
    """Регистрация админских хендлеров."""
    dp.register_message_handler(cancel_handler, filters.Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(greeting, commands=["start"], state="*")
    dp.register_message_handler(make_record, text='Редактировать информацию о студенте', state=None)
    dp.register_message_handler(get_student_info, text='Уточнить информацию о студенте', state=None)
    dp.register_message_handler(obtain_prof_id, filters.Regexp(r'\b\d{2}-\d{4}\b'), state=MakeRecordFSM.waiting_prof_id)
    dp.register_message_handler(obtain_change_pole, content_types=['text'], state=MakeRecordFSM.waiting_change_pole)
    dp.register_message_handler(obtain_new_value, content_types=['text'], state=MakeRecordFSM.waiting_new_value)
    dp.register_message_handler(obtain_confirm, content_types=['text'], state=MakeRecordFSM.waiting_confirm)
    dp.register_message_handler(obtain_pole_name, content_types=['text'], state=GetStudentInfoFSM.waiting_pole_name)
    dp.register_message_handler(obtain_value, content_types=['text'], state=GetStudentInfoFSM.waiting_value)
