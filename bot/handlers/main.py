from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import StatesGroup, State

from utils import keyboards, request_funcs
from bot_run import bot
from utils.lang_parser import get_phrase
from utils.check_role import super_admin_require


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Выход из машины состояний. """

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    check = await request_funcs.get_student_info("telegram_id", message.from_user.id)
    if isinstance(check, list):
        await bot.send_message(message.from_user.id, get_phrase('ok'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, get_phrase('ok'),
                               reply_markup=keyboards.REGISTRATION_KEYBOARD)


async def greeting(message: types.Message, state: FSMContext) -> None:
    """Отлавливает команду /start, выводит соответствующую клавиатуру."""

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    check = await request_funcs.get_student_info("telegram_id", message.from_user.id)
    if isinstance(check, list):
        await bot.send_message(message.from_user.id, get_phrase('greeting_after_registration'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, get_phrase('greeting_reg_ask'))
        await bot.send_message(message.from_user.id, get_phrase('ask_personal_agreement'),
                               reply_markup=keyboards.REGISTRATION_KEYBOARD)
    await message.delete()


@super_admin_require
async def super_admin_help(message: types.Message, state: FSMContext):
    """ Отлавливает "/help" от супер-админа, выдаёт список команд. """

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await bot.send_message(message.from_user.id, get_phrase('superadmin_help'),
                           reply_markup=await keyboards.keyboard_choice(message.from_user.id))


class RegistrationFSM(StatesGroup):
    """Машина состояний - диалог регистрации."""
    waiting_stud_info = State()


async def registration(message: types.Message, state: FSMContext) -> None:
    """Начало диалога регистрации, делаем запрос на сервер с целью определить нет ли такого id в бд."""

    res = await request_funcs.get_student_info("telegram_id", message.from_user.id)

    if isinstance(res, list):
        await bot.send_message(message.from_user.id, get_phrase('registration_already_passed'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, get_phrase('enter_your_student_book'))
        await RegistrationFSM.waiting_stud_info.set()


async def obtain_stud_info(message: types.Message, state: FSMContext) -> None:
    """Отлавливает номер студенческого при запущенном диалоге RegistrationFSM, вносит ин-фу в бд."""

    stud_id = message.text
    telegram_id = message.from_user.id
    stud_info = await request_funcs.get_student_info("Студенческий билет", stud_id)

    if isinstance(stud_info, list):
        bd_id = stud_info[0]["id"]
        await request_funcs.redact_student_info(bd_id, 'telegram_id', telegram_id)
        await bot.send_message(message.from_user.id, get_phrase('registration_passed'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, get_phrase('registration_mistake'),
                               reply_markup=keyboards.REGISTRATION_KEYBOARD)
    await state.finish()


def register_main_handlers(dp: Dispatcher) -> None:
    """Регистрация основных хендлеров."""
    dp.register_message_handler(cancel_handler, filters.Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(greeting, commands=["start"], state="*")
    dp.register_message_handler(super_admin_help, commands=['help'], state="*")
    dp.register_message_handler(registration, text=['Регистрация'])
    dp.register_message_handler(obtain_stud_info, content_types=['text'],
                                state=RegistrationFSM.waiting_stud_info)


async def wtf_answering(message: types.Message, state: FSMContext) -> None:
    """Ответ на непонятные сообщения"""
    await bot.send_message(message.from_user.id, get_phrase('not_understand'))


def register_wtf_handler(dp: Dispatcher) -> None:
    """Регистрация основных хендлеров."""
    dp.register_message_handler(wtf_answering, state="*")
