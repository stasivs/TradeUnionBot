from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_run import bot
from utils import keyboards, request_funcs
from utils.check_role import admin_require
from utils.lang_parser import get_phrase


class GetStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог предоставления ин-фы о студенте."""
    waiting_pole_name = State()
    waiting_value = State()


@admin_require
async def get_student_info(message: types.Message) -> None:
    """Отлавливает соответствующий текст кнопки, запускает диалог предоставления ин-фы о студенте."""

    await bot.send_message(message.from_user.id, get_phrase('choose_field_for_search'),
                           reply_markup=keyboards.INFO_POLE_KEYBOARD)
    await GetStudentInfoFSM.waiting_pole_name.set()


async def obtain_pole_name(message: types.Message, state: FSMContext) -> None:
    """Отлавливает название известного поля, вносит в state.proxy()."""

    async with state.proxy() as data:
        data['pole_name'] = message.text

    if data['pole_name'] == 'Проф карта':
        await bot.send_message(message.from_user.id, get_phrase('enter_profcard'),
                               reply_markup=keyboards.CANCEL_KEYBOARD)

    elif data['pole_name'] == 'Студенческий билет':
        await bot.send_message(message.from_user.id, get_phrase('enter_student_book'),
                               reply_markup=keyboards.CANCEL_KEYBOARD)

    elif data['pole_name'] == 'Фамилия студента':
        await bot.send_message(message.from_user.id, get_phrase('enter_surname'),
                               reply_markup=keyboards.CANCEL_KEYBOARD)

    elif data['pole_name'] == 'ФИО студента':
        await bot.send_message(message.from_user.id, get_phrase('enter_fio'),
                               reply_markup=keyboards.CANCEL_KEYBOARD)

    await GetStudentInfoFSM.next()


async def obtain_value(message: types.Message, state: FSMContext) -> None:
    """
    Отлавливает значение известного поля, вносит в state.proxy(),
    вызывает соответствующую функцию обращения к серверу, выводит информацию о студенте,
    выдаёт инлайн кнопку для суперадмина
    """
    async with state.proxy() as data:
        data['value'] = message.text.title()
        response = await request_funcs.get_student_info(data['pole_name'], data['value'])

    if isinstance(response, list):
        for student in response:
            await bot.send_message(message.from_user.id, get_phrase('stud_info',
                                                                    student['group'],
                                                                    student['surname'],
                                                                    student['name'].split()[0],
                                                                    student['name'].split()[1],
                                                                    student['sex'],
                                                                    student['financing_form'],
                                                                    student['profcard'],
                                                                    student['student_book'],
                                                                    student['role']),
                                   reply_markup=await keyboards.inline_keyboard_choice(message.from_user.id,
                                                                                       student["id"]))

        await bot.send_message(message.from_user.id, get_phrase('students_shown'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

        await state.finish()

    elif response == 404:
        await bot.send_message(message.from_user.id, get_phrase('students_not_found'),
                               reply_markup=keyboards.CANCEL_KEYBOARD)

    else:
        await bot.send_message(message.from_user.id, get_phrase('input_mistake_phrase'),
                               reply_markup=keyboards.CANCEL_KEYBOARD)


def register_admin_handlers(dp: Dispatcher) -> None:
    """Регистрация админских хендлеров."""
    dp.register_message_handler(get_student_info, text='Поиск по базе данных', state=None)
    dp.register_message_handler(obtain_pole_name, lambda x: x.text in ['Проф карта', 'Студенческий билет',
                                                                       'Фамилия студента', 'ФИО студента'],
                                state=GetStudentInfoFSM.waiting_pole_name)
    dp.register_message_handler(obtain_value, content_types=['text'],
                                state=GetStudentInfoFSM.waiting_value)
