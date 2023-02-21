from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters

from utils import keyboards, request_funcs
from bot_run import bot
from utils.lang_parser import get_phrase


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Выход из машины состояний. """

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    check = await request_funcs.get_student_info("telegram_id", message.from_user.id)
    if check:
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
    if check:
        await bot.send_message(message.from_user.id, get_phrase('greeting_after_registration'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, get_phrase('greeting_reg_ask'))
        await bot.send_message(message.from_user.id, get_phrase('ask_personal_agreement'),
                               reply_markup=keyboards.REGISTRATION_KEYBOARD)
    await message.delete()


def register_main_handlers(dp: Dispatcher) -> None:
    """Регистрация основных хендлеров."""
    dp.register_message_handler(cancel_handler, filters.Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(greeting, commands=["start"], state="*")


async def wtf_answering(message: types.Message, state: FSMContext) -> None:
    """Ответ на непонятные сообщения"""
    await bot.send_message(message.from_user.id, get_phrase('not_understand'))


def register_wtf_handler(dp: Dispatcher) -> None:
    """Регистрация основных хендлеров."""
    dp.register_message_handler(wtf_answering, state="*")
