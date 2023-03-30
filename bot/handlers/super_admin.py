from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_init import bot
from utils import keyboards, request_funcs
from utils.check_role import super_admin_require, redis
from utils.csv_parser import csv_parser
from utils.lang_parser import get_phrase


class RedactStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог редактирования ин-фы о студенте."""

    redact_student_info = State()
    waiting_change_pole = State()
    waiting_new_value = State()
    waiting_confirm = State()


@super_admin_require
async def redact_student_info(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    """Отлавливает соответствующий посыл инлайн-кнопки, запускает диалог внесения изменений в бд."""

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await RedactStudentInfoFSM.redact_student_info.set()

    async with state.proxy() as data:
        callback_data = callback_query.data.replace("redact ", "").split()
        data["bd_id"] = callback_data[0]
        data["cur_telegram_id"] = callback_data[1] if len(callback_data) > 1 else None

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=get_phrase("choose_field_for_change"),
        reply_markup=keyboards.CHANGE_POLE_KEYBOARD,
    )

    await RedactStudentInfoFSM.next()


async def obtain_change_pole(message: types.Message, state: FSMContext) -> None:
    """Отлавливает название поля для последующего изменения, вносит в state.proxy()."""

    async with state.proxy() as data:
        data["pole_name"] = message.text

    if data["pole_name"] in [
        "Проф карта",
        "Студенческий билет",
        "Телеграм ID",
        "Комментарий",
        "Фамилия студента",
        "Имя студента",
        "Отчество студента",
        "ИКГ",
    ]:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("enter_new_value", data["pole_name"]),
            reply_markup=keyboards.CANCEL_KEYBOARD,
        )

    elif data["pole_name"] == "Роль пользователя":
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("enter_new_value", data["pole_name"]),
            reply_markup=keyboards.ROLE_KEYBOARD,
        )

    elif data["pole_name"] == "Форма финансирования":
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("enter_new_value", data["pole_name"]),
            reply_markup=keyboards.FINANCING_FORM_KEYBOARD,
        )

    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("not_such_pole"),
            reply_markup=await keyboards.keyboard_choice(message.from_user.id),
        )
        await state.finish()

    await RedactStudentInfoFSM.next()


async def obtain_new_value(message: types.Message, state: FSMContext) -> None:
    """Отлавливает новое значение для ранее выбранного поля, вносит в state.proxy()."""

    async with state.proxy() as data:
        if data["pole_name"] not in [
            "Комментарий",
            "Роль пользователя",
            "Форма финансирования",
            "ИКГ",
        ]:
            data["new_value"] = message.text.title()
        else:
            data["new_value"] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_phrase("ask_confirm", data["pole_name"], data["new_value"]),
        reply_markup=keyboards.APPROVAL_KEYBOARD,
    )
    await RedactStudentInfoFSM.next()


async def obtain_confirm(message: types.Message, state: FSMContext) -> None:
    """Отлавливает подтверждение команды об изменении бд, вызывает соответствующую функцию обращения к серверу."""

    if message.text.lower() == "да":
        async with state.proxy() as data:
            response = await request_funcs.redact_student_info(
                bd_id=data["bd_id"],
                pole_name=data["pole_name"],
                new_value=data["new_value"],
            )

            if response:
                if data["cur_telegram_id"]:
                    await redis.delete(data["cur_telegram_id"])

                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=get_phrase("changes_done"),
                    reply_markup=await keyboards.keyboard_choice(message.from_user.id),
                )
            else:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=get_phrase("input_mistake_phrase"),
                    reply_markup=await keyboards.keyboard_choice(message.from_user.id),
                )

    elif message.text.lower() == "нет":
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("ok"),
            reply_markup=await keyboards.keyboard_choice(message.from_user.id),
        )

    await state.finish()


class AddManyStudentsInfoFSM(StatesGroup):
    """Машина состояний - диалог добавления ин-фы о студентах."""

    waiting_csv_file = State()


@super_admin_require
async def add_many_students_info(message: types.Message, state: FSMContext) -> None:
    """Отлавливает команду '/add_students_data'."""

    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_phrase("ask_file"),
        reply_markup=keyboards.CANCEL_KEYBOARD,
    )
    await AddManyStudentsInfoFSM.waiting_csv_file.set()


async def get_csv_file(message: types.Message, state: FSMContext) -> None:
    """Отлавливает csv файл."""

    if message.document.file_name.endswith(".csv"):
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("wait"),
            reply_markup=await keyboards.keyboard_choice(message.from_user.id),
        )

        with await bot.download_file_by_id(message.document.file_id) as file:
            res = await request_funcs.add_many_student_data(
                await csv_parser(str(file.read(), "utf-8"))
            )
            if res:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=get_phrase(
                        "bd_update_success", str(res["students_added_counter"])
                    ),
                    reply_markup=await keyboards.keyboard_choice(message.from_user.id),
                )
            else:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=get_phrase("bd_update_fail"),
                    reply_markup=await keyboards.keyboard_choice(message.from_user.id),
                )

    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("wrong_format"),
            reply_markup=await keyboards.keyboard_choice(message.from_user.id),
        )

    await state.finish()


class RedactScheduleFSM(StatesGroup):
    """Машина состояний - диалог редактирования расписания приёма документов."""

    waiting_institute_name = State()
    waiting_image_id = State()


@super_admin_require
async def redact_schedule(message: types.Message, state: FSMContext) -> None:
    """Отлавливает команду '/redact_schedule'."""

    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_phrase("choose_institute_name"),
        reply_markup=keyboards.INSTITUTE_NAME_KEYBOARD,
    )
    await RedactScheduleFSM.waiting_institute_name.set()


async def obtain_institute_name(message: types.Message, state: FSMContext) -> None:
    """Отлавливает имя института, вносит в state.proxy()."""

    async with state.proxy() as data:
        data["institute_name"] = message.text

    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_phrase("send_schedule_image"),
        reply_markup=keyboards.CANCEL_KEYBOARD,
    )

    await RedactScheduleFSM.next()


async def obtain_image_id(message: types.Message, state: FSMContext) -> None:
    """Отлавливает изображение, вносит его id в state.proxy(), отправляет на сервер."""

    async with state.proxy() as data:
        data["image_id"] = message.photo[0].file_id
        response = await request_funcs.redact_profcome_schedule(
            institute_name=data["institute_name"], image_id=data["image_id"]
        )

    if response:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("schedule_update_success"),
            reply_markup=await keyboards.keyboard_choice(message.from_user.id),
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("schedule_update_fail"),
            reply_markup=await keyboards.keyboard_choice(message.from_user.id),
        )

    await state.finish()


@super_admin_require
async def database_provide(message: types.Message, state: FSMContext) -> None:
    response = await request_funcs.get_database()

    if response:
        await bot.send_document(
            chat_id=message.from_user.id,
            document=("database.csv", response.content),
            reply_markup=await keyboards.keyboard_choice(message.from_user.id),
        )

    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=get_phrase("get_database_mistake"),
            reply_markup=await keyboards.keyboard_choice(message.from_user.id),
        )


def register_super_admin_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        redact_student_info,
        lambda x: x.data and x.data.startswith("redact "),
        state="*",
    )
    dp.register_message_handler(
        obtain_change_pole,
        content_types=["text"],
        state=RedactStudentInfoFSM.waiting_change_pole,
    )
    dp.register_message_handler(
        obtain_new_value,
        content_types=["text"],
        state=RedactStudentInfoFSM.waiting_new_value,
    )
    dp.register_message_handler(
        obtain_confirm,
        lambda x: x.text in ["Да", "Нет", "да", "нет"],
        state=RedactStudentInfoFSM.waiting_confirm,
    )
    dp.register_message_handler(add_many_students_info, commands=["add_students_data"])
    dp.register_message_handler(
        get_csv_file,
        content_types=["document"],
        state=AddManyStudentsInfoFSM.waiting_csv_file,
    )
    dp.register_message_handler(redact_schedule, commands=["redact_schedule"])
    dp.register_message_handler(
        obtain_institute_name,
        content_types=["text"],
        state=RedactScheduleFSM.waiting_institute_name,
    )
    dp.register_message_handler(
        obtain_image_id,
        content_types=["photo"],
        state=RedactScheduleFSM.waiting_image_id,
    )
    dp.register_message_handler(database_provide, commands=["get_the_current_database"])
