from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import StatesGroup, State

from utils import keyboards, request_funcs
from bot_init import bot
from utils.lang_parser import get_phrase
from utils.check_role import super_admin_require


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Выход из машины состояний. """

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await bot.send_message(message.from_user.id, get_phrase('ok'),
                           reply_markup=await keyboards.keyboard_choice(message.from_user.id))


async def greeting(message: types.Message, state: FSMContext) -> None:
    """Отлавливает команду /start, выводит соответствующую клавиатуру."""

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    check = await request_funcs.get_student_info("Телеграм ID", message.from_user.id)
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
    waiting_confirm = State()


async def registration(message: types.Message, state: FSMContext) -> None:
    """Начало диалога регистрации, делаем запрос на сервер с целью определить нет ли такого id в бд."""

    res = await request_funcs.get_student_info("Телеграм ID", message.from_user.id)

    if isinstance(res, list):
        await bot.send_message(message.from_user.id, get_phrase('registration_already_passed'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, get_phrase('enter_your_student_book'))
        await RegistrationFSM.waiting_stud_info.set()


async def obtain_stud_info(message: types.Message, state: FSMContext) -> None:
    """Отлавливает номер студенческого при запущенном диалоге RegistrationFSM, проверяет на наличие
    такого студенческого в бд, проверяет, что это не админ, вносит ин-фу в бд."""

    stud_id = message.text.title()
    stud_info = await request_funcs.get_student_info("Студенческий билет", stud_id)

    if isinstance(stud_info, list):
        if stud_info[0]['role'] in ['Admin', 'SuperAdmin']:
            await bot.send_message(message.from_user.id, get_phrase('try_of_admin_registration_mistake'),
                                   reply_markup=keyboards.REGISTRATION_KEYBOARD)
            await state.finish()
        else:
            async with state.proxy() as data:
                data['bd_id'] = stud_info[0]['id']

            student_fio = ' '.join(
                [stud_info[0]['surname'], stud_info[0]['name'], stud_info[0]['second_name']])  # возможна ошибка
            await bot.send_message(message.from_user.id, get_phrase('registration_confirm_require', student_fio),
                                   reply_markup=keyboards.APPROVAL_KEYBOARD)
            await RegistrationFSM.next()

    else:
        await bot.send_message(message.from_user.id, get_phrase('input_mistake_phrase'))


async def obtain_confirm(message: types.Message, state: FSMContext) -> None:
    """Отлавливает подтверждение команды о регистрации, вызывает соответствующую функцию обращения к серверу."""

    if message.text.lower() == 'да':
        async with state.proxy() as data:
            bd_id = data["bd_id"]
        telegram_id = message.from_user.id

        response = await request_funcs.redact_student_info(bd_id, 'Телеграм ID', telegram_id)

        if response:
            await bot.send_message(message.from_user.id, get_phrase('registration_passed'),
                                   reply_markup=await keyboards.keyboard_choice(message.from_user.id))
        else:
            await bot.send_message(message.from_user.id, get_phrase('registration_passing_mistake'),
                                   reply_markup=keyboards.REGISTRATION_KEYBOARD)

    elif message.text.lower() == 'нет':
        await bot.send_message(message.from_user.id, get_phrase('input_mistake_phrase'),
                               reply_markup=keyboards.REGISTRATION_KEYBOARD)

    await state.finish()


def register_main_handlers(dp: Dispatcher) -> None:
    """Регистрация основных хендлеров."""
    dp.register_message_handler(cancel_handler, lambda x: x.text in ['Отмена', 'В главное меню'], state='*')
    dp.register_message_handler(greeting, commands=["start"], state="*")
    dp.register_message_handler(super_admin_help, commands=['help'], state="*")
    dp.register_message_handler(registration, text=['Регистрация'])
    dp.register_message_handler(obtain_stud_info, content_types=['text'],
                                state=RegistrationFSM.waiting_stud_info)
    dp.register_message_handler(obtain_confirm, lambda x: x.text in ['Да', 'Нет', 'да', 'нет'],
                                state=RegistrationFSM.waiting_confirm)


async def wtf_answering(message: types.Message, state: FSMContext) -> None:
    """Ответ на непонятные сообщения"""
    await bot.send_message(message.from_user.id, get_phrase('not_understand'),
                           reply_markup=await keyboards.keyboard_choice(message.from_user.id))


def register_wtf_handler(dp: Dispatcher) -> None:
    """Регистрация основных хендлеров."""
    dp.register_message_handler(wtf_answering, state="*")
