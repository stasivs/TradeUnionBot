from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from bot_run import bot
from utils import keyboards, request_funcs


async def get_profcome_schedule(message: types.Message) -> None:
    """Отлавливает и выполняет команду о предоставлении расписания"""
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00',
                           reply_markup=await keyboards.keyboard_choice(message.from_user.id))


async def get_prof_id(message: types.Message) -> None:
    """Отлавливает команду о предоставлении номера профкарты, используя id пользователя
    вызывает соответствующую функцию обращения к серверу."""
    stud_info = await request_funcs.get_student_info('telegram_id', message.from_user.id)
    prof_id = stud_info['prof_id']
    if prof_id:
        await bot.send_message(message.from_user.id, f'Номер профкарты: {prof_id}',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, 'Пройдите регистрацию',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))


class RegistrationFSM(StatesGroup):
    """Машина состояний - диалог регистрации."""
    waiting_stud_info = State()


async def registration(message: types.Message) -> None:
    """Начало диалога регистрации."""
    await RegistrationFSM.waiting_stud_info.set()
    await message.reply('Введите номер студенческого билета', reply_markup=ReplyKeyboardRemove())


async def obtain_stud_info(message: types.Message, state: FSMContext) -> None:
    """Отлавливает номер студенческого при запущенном диалоге RegistrationFSM, вносит ин-фу в бд"""
    stud_id = message.text
    telegram_id = message.from_user.id
    await request_funcs.redact_student_info(stud_id, 'telegram_id', telegram_id)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Регистрация пройдена',
                           reply_markup=keyboards.keyboard_choice(message.from_user.id))


def register_student_handlers(dp: Dispatcher) -> None:
    """Регистрация студенческих хендлеров."""
    dp.register_message_handler(get_profcome_schedule, text=['Узнать расписание профкома'])
    dp.register_message_handler(get_prof_id, text=['Узнать номер своей профкарты'])
    dp.register_message_handler(registration, text=['Пройти регистрацию'])
    dp.register_message_handler(obtain_stud_info, filters.Regexp(r'\b\d{2}-[А-Я]-\d{5}\b'),
                                state=RegistrationFSM.waiting_stud_info)
