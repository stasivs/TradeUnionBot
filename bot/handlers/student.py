import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_run import bot
from utils import keyboards, request_funcs


class GetProfcomeScheduleFSM(StatesGroup):
    """Машина состояний - диалог предоставления ин-фы о студенте."""
    waiting_institute_name = State()


async def get_profcome_schedule(message: types.Message) -> None:
    """Отлавливает команду о предоставлении расписания, запускает соответствующий диалог."""
    logging.info("get schedule button")
    await bot.send_message(message.from_user.id, 'Выберите свой институт',
                           reply_markup=keyboards.INSTITUTE_NAME_KEYBOARD)
    await GetProfcomeScheduleFSM.waiting_institute_name.set()


async def obtain_institute_name(message: types.Message, state: FSMContext) -> None:
    """Отлавливает имя института и выдаёт соответствующее расписане."""
    profcome_schedule = await request_funcs.get_profcome_schedule(message.text)
    if profcome_schedule:
        response = f'Расписание для {profcome_schedule["institute"]}: {profcome_schedule["timetable"]}'
        await bot.send_message(message.from_user.id, response,
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, "Приношу извинения, в данный момент расписание недоступно",
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    await state.finish()


async def get_prof_id(message: types.Message) -> None:
    """Отлавливает команду о предоставлении номера профкарты, используя id пользователя
    вызывает соответствующую функцию обращения к серверу."""
    logging.info("get prof id button")
    stud_info = await request_funcs.get_student_info('telegram_id', message.from_user.id)
    if stud_info:
        prof_id = stud_info[0]['profcard']
        await bot.send_message(message.from_user.id, f'Номер профкарты: {prof_id}',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, 'Пройдите регистрацию',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))


class RegistrationFSM(StatesGroup):
    """Машина состояний - диалог регистрации."""
    waiting_stud_info = State()


async def registration(message: types.Message, state: FSMContext) -> None:
    """Начало диалога регистрации, делаем запрос на сервер с целью определить нет ли такого id в бд."""
    logging.info("registration button")
    res = await request_funcs.get_student_info("telegram_id", message.from_user.id)
    if res:
        await bot.send_message(message.from_user.id, 'Вы уже прошли регистрацию',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, 'Введите номер своего студенческого билета')
        await RegistrationFSM.waiting_stud_info.set()


async def obtain_stud_info(message: types.Message, state: FSMContext) -> None:
    """Отлавливает номер студенческого при запущенном диалоге RegistrationFSM, вносит ин-фу в бд."""
    stud_id = message.text
    telegram_id = message.from_user.id
    stud_info = await request_funcs.get_student_info("Студенческий билет", stud_id)
    if stud_info:
        bd_id = stud_info[0]["id"]
        await request_funcs.redact_student_info(bd_id, 'telegram_id', telegram_id)
        await bot.send_message(message.from_user.id, 'Регистрация пройдена',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, 'Что-то не так, возможно, вас ещё нет у нас в базе данных',
                               reply_markup=keyboards.REGISTRATION_KEYBOARD)
    await state.finish()


def register_student_handlers(dp: Dispatcher) -> None:
    """Регистрация студенческих хендлеров."""
    dp.register_message_handler(get_profcome_schedule, text=['Узнать расписание приёма документов'], state=None)
    dp.register_message_handler(obtain_institute_name, content_types=['text'],
                                state=GetProfcomeScheduleFSM.waiting_institute_name)
    dp.register_message_handler(get_prof_id, text=['Узнать номер своей профкарты'])
    dp.register_message_handler(registration, text=['Регистрация'])
    dp.register_message_handler(obtain_stud_info, filters.Regexp(r'\b\d{2}-[А-Я]-\d{5}\b'),
                                state=RegistrationFSM.waiting_stud_info)
