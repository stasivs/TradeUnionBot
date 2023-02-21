from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_run import bot
from utils import keyboards, request_funcs
from utils.lang_parser import get_phrase


class GetProfcomeScheduleFSM(StatesGroup):
    """Машина состояний - диалог предоставления ин-фы о студенте."""
    waiting_institute_name = State()


async def get_profcome_schedule(message: types.Message) -> None:
    """Отлавливает команду о предоставлении расписания, запускает соответствующий диалог."""

    await bot.send_message(message.from_user.id, get_phrase('choose_institute_name'),
                           reply_markup=keyboards.INSTITUTE_NAME_KEYBOARD)
    await GetProfcomeScheduleFSM.waiting_institute_name.set()


async def obtain_institute_name(message: types.Message, state: FSMContext) -> None:
    """Отлавливает имя института и выдаёт соответствующее расписание."""

    response = await request_funcs.get_profcome_schedule(message.text)

    if response:
        await bot.send_photo(message.from_user.id, response['timetable'],
                             reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    else:
        await bot.send_message(message.from_user.id, get_phrase('schedule_not_available'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    await state.finish()


async def get_prof_id(message: types.Message) -> None:
    """Отлавливает команду о предоставлении номера профкарты, используя id пользователя
    вызывает соответствующую функцию обращения к серверу."""

    stud_info = await request_funcs.get_student_info('telegram_id', message.from_user.id)

    if stud_info:
        prof_id = stud_info[0]['profcard']
        await bot.send_message(message.from_user.id, get_phrase('profcard_output', prof_id),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, get_phrase('registration_require'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))


class RegistrationFSM(StatesGroup):
    """Машина состояний - диалог регистрации."""
    waiting_stud_info = State()


async def registration(message: types.Message, state: FSMContext) -> None:
    """Начало диалога регистрации, делаем запрос на сервер с целью определить нет ли такого id в бд."""

    res = await request_funcs.get_student_info("telegram_id", message.from_user.id)

    if res:
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

    if stud_info:
        bd_id = stud_info[0]["id"]
        await request_funcs.redact_student_info(bd_id, 'telegram_id', telegram_id)
        await bot.send_message(message.from_user.id, get_phrase('registration_passed'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, get_phrase('registration_mistake'),
                               reply_markup=keyboards.REGISTRATION_KEYBOARD)
    await state.finish()


def register_student_handlers(dp: Dispatcher) -> None:
    """Регистрация студенческих хендлеров."""
    dp.register_message_handler(get_profcome_schedule, text=['Узнать расписание приёма документов'], state=None)
    dp.register_message_handler(obtain_institute_name, content_types=['text'],
                                state=GetProfcomeScheduleFSM.waiting_institute_name)
    dp.register_message_handler(get_prof_id, text=['Узнать номер своей профкарты'])
    dp.register_message_handler(registration, text=['Регистрация'])
    dp.register_message_handler(obtain_stud_info, content_types=['text'],
                                state=RegistrationFSM.waiting_stud_info)
