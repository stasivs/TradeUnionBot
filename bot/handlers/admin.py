from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_init import bot
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

    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_phrase("choose_field_for_search"),
        reply_markup=keyboards.INFO_POLE_KEYBOARD,
    )
    await GetStudentInfoFSM.waiting_pole_name.set()


async def obtain_pole_name(message: types.Message, state: FSMContext) -> None:
    """Отлавливает название известного поля, вносит в state.proxy()."""

    async with state.proxy() as data:
        data["pole_name"] = message.text

    pole_names_dict = {
        "Проф карта": "enter_profcard",
        "Студенческий билет": "enter_student_book",
        "Фамилия студента": "enter_surname",
        "ФИО студента": "enter_fio",
    }

    try:
        phrase = pole_names_dict[data["pole_name"]]
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase(phrase),
            reply_markup=keyboards.CANCEL_KEYBOARD,
        )
        await GetStudentInfoFSM.next()

    except KeyError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("not_such_pole"),
            reply_markup=await keyboards.keyboard_choice(message.from_user.id),
        )
        await state.finish()


async def obtain_value(message: types.Message, state: FSMContext) -> None:
    """
    Отлавливает значение известного поля, вносит в state.proxy(),
    вызывает соответствующую функцию обращения к серверу, выводит информацию о студенте,
    выдаёт инлайн кнопку для суперадмина.
    """
    async with state.proxy() as data:
        data["value"] = message.text.title()
        response = await request_funcs.get_student_info(
            pole_name=data["pole_name"], value=data["value"]
        )

    if isinstance(response, list):
        for student in response:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=get_phrase(
                    "stud_info",
                    student["group"] if student["group"] else "Отсутствует",
                    student["surname"] if student["surname"] else "Отсутствует",
                    student["name"] if student["name"] else "Отсутствует",
                    student["second_name"] if student["second_name"] else "Отсутствует",
                    student["birthdate"] if student["birthdate"] else "Отсутствует",
                    student["sex"] if student["sex"] else "Отсутствует",
                    student["financing_form"]
                    if student["financing_form"]
                    else "Отсутствует",
                    student["profcard"] if student["profcard"] else "Отсутствует",
                    student["student_book"]
                    if student["student_book"]
                    else "Отсутствует",
                    student["role"] if student["role"] else "Отсутствует",
                    student["telegram_id"] if student["telegram_id"] else "Отсутствует",
                    student["comment"] if student["comment"] else "Отсутствует",
                ),
                reply_markup=await keyboards.inline_keyboard_choice(
                    user_id=message.from_user.id,
                    student_bd_id=student["id"],
                    telegram_id=student["telegram_id"],
                ),
            )

        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("students_shown"),
            reply_markup=await keyboards.keyboard_choice(message.from_user.id),
        )

        await state.finish()

    elif response == 404:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("students_not_found"),
            reply_markup=keyboards.CANCEL_KEYBOARD,
        )

    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("input_mistake_phrase"),
            reply_markup=keyboards.CANCEL_KEYBOARD,
        )


def register_admin_handlers(dp: Dispatcher) -> None:
    """Регистрация админских хендлеров."""
    dp.register_message_handler(
        get_student_info, text="Поиск по базе данных", state=None
    )
    dp.register_message_handler(
        obtain_pole_name,
        content_types=["text"],
        state=GetStudentInfoFSM.waiting_pole_name,
    )
    dp.register_message_handler(
        obtain_value, content_types=["text"], state=GetStudentInfoFSM.waiting_value
    )
