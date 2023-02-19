from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_run import bot
from utils import keyboards, request_funcs
from utils.check_role import super_admin_require, redis
from utils.csv_parser import csv_parser


class RedactStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог редактирования ин-фы о студенте."""
    redact_student_info = State()
    waiting_change_pole = State()
    waiting_new_value = State()
    waiting_confirm = State()


@super_admin_require
async def redact_student_info(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Отлавливает соответствующий посыл инлайн-кнопки, запускает диалог внесения изменений в бд."""

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await RedactStudentInfoFSM.redact_student_info.set()
    async with state.proxy() as data:
        data['bd_id'] = callback_query.data.replace('redact ', '')

    await bot.send_message(callback_query.from_user.id, 'Выберите поле, в которое хотите внести изменения',
                           reply_markup=keyboards.CHANGE_POLE_KEYBOARD)
    await RedactStudentInfoFSM.next()


async def obtain_change_pole(message: types.Message, state: FSMContext) -> None:
    """Отлавливает название поля для последующего изменения, вносит в state.proxy()."""

    async with state.proxy() as data:
        data['pole_name'] = message.text

    if data['pole_name'] == 'Проф карта':
        await bot.send_message(message.from_user.id, 'Введите новое значение поля "Проф карта", '
                                                     'формат: 00-0000"',
                               reply_markup=keyboards.CANCEL_KEYBOARD)

    elif data['pole_name'] == 'Студенческий билет':
        await bot.send_message(message.from_user.id, 'Введите новое значение поля "Студенческий билет", '
                                                     'формат: 00-А-00000"',
                               reply_markup=keyboards.CANCEL_KEYBOARD)

    elif data['pole_name'] == 'Причина мат помощи':
        await bot.send_message(message.from_user.id, f'Введите новое значение поля "Причина мат помощи"',
                               reply_markup=keyboards.CANCEL_KEYBOARD)

    elif data['pole_name'] == 'Роль пользователя':
        await bot.send_message(message.from_user.id, f'Введите новое значение поля "Роль пользователя"',
                               reply_markup=keyboards.ROLE_KEYBOARD)

    await RedactStudentInfoFSM.next()


async def obtain_new_value(message: types.Message, state: FSMContext) -> None:
    """Отлавливает новое значение для ранее выбранного поля, вносит в state.proxy()."""

    async with state.proxy() as data:
        data['new_value'] = message.text

    await bot.send_message(message.from_user.id, f'Внести изменения: {data["pole_name"]} -> {data["new_value"]} ?',
                           reply_markup=keyboards.APPROVAL_KEYBOARD)
    await RedactStudentInfoFSM.next()


async def obtain_confirm(message: types.Message, state: FSMContext) -> None:
    """Отлавливает подтверждение команды об изменении бд, вызывает соответствующую функцию обращения к серверу."""

    if message.text.lower() == 'да':
        async with state.proxy() as data:
            response = await request_funcs.redact_student_info(data['bd_id'], data['pole_name'], data['new_value'])

            if response:

                if response[0]['telegram_id']:
                    await redis.delete(response[0]['telegram_id'])

                await bot.send_message(message.from_user.id, 'Изменения внесены',
                                       reply_markup=await keyboards.keyboard_choice(message.from_user.id))
            else:
                await bot.send_message(message.from_user.id, 'Что-то не так, возможно, вы ошиблись при вводе данных',
                                       reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    elif message.text.lower() == 'нет':
        await bot.send_message(message.from_user.id, 'OK',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    await state.finish()


class AddStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог добавления ин-фы о студентах."""
    waiting_csv_file = State()


@super_admin_require
async def add_many_students_info(message: types.Message, state: FSMContext) -> None:
    """Отлавливает команду '/add_students_data'."""

    await bot.send_message(message.from_user.id, 'Отправьте файл в формате "CSV" с информацией о студентах',
                           reply_markup=keyboards.CANCEL_KEYBOARD)
    await AddStudentInfoFSM.waiting_csv_file.set()


async def get_csv_file(message: types.Message, state: FSMContext) -> None:
    if message.document.file_name.endswith('.csv'):
        await bot.send_message(message.from_user.id, 'Ожидайте...',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

        with await bot.download_file_by_id(message.document.file_id) as file:
            res = await request_funcs.add_many_student_data(await csv_parser(str(file.read(), 'utf-8')))
            if res:
                await bot.send_message(message.from_user.id,
                                       f'Успешно добавлена информация о {res["students_added_counter"]} студентах',
                                       reply_markup=await keyboards.keyboard_choice(message.from_user.id))
            else:
                await bot.send_message(message.from_user.id, 'Не удалось добавить информацию',
                                       reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    else:
        await bot.send_message(message.from_user.id, 'Неправильный формат файла',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    await state.finish()


class RedactScheduleFSM(StatesGroup):
    """Машина состояний - диалог редактирования расписания приёма документов."""
    waiting_institute_name = State()
    waiting_image_id = State()


@super_admin_require
async def redact_schedule(message: types.Message, state: FSMContext) -> None:
    """Отлавливает команду '/redact_schedule'."""

    await bot.send_message(message.from_user.id, 'Выберите название института',
                           reply_markup=keyboards.INSTITUTE_NAME_KEYBOARD)
    await RedactScheduleFSM.waiting_institute_name.set()


async def obtain_institute_name(message: types.Message, state: FSMContext) -> None:
    """Отлавливает имя института, вносит в state.proxy()."""

    async with state.proxy() as data:
        data['institute_name'] = message.text

    await bot.send_message(message.from_user.id, 'Отправьте изображение с расписанием',
                           reply_markup=keyboards.CANCEL_KEYBOARD)

    await RedactScheduleFSM.next()


async def obtain_image_id(message: types.Message, state: FSMContext) -> None:
    """Отлавливает изображение, вносит его id в state.proxy(), отправляет на сервер."""

    async with state.proxy() as data:
        data['image_id'] = message.photo[0].file_id
        response = await request_funcs.redact_profcome_schedule(data['institute_name'], data['image_id'])

    if response:
        await bot.send_message(message.from_user.id, f'Расписание установлено',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, f'Не удалось установить расписание',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    await state.finish()


def register_super_admin_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(redact_student_info, lambda x: x.data and x.data.startswith('redact '),
                                       state='*')
    dp.register_message_handler(obtain_change_pole,
                                lambda x: x.text in ['Проф карта', 'Студенческий билет', 'Причина мат помощи',
                                                     'Роль пользователя'],
                                state=RedactStudentInfoFSM.waiting_change_pole)
    dp.register_message_handler(obtain_new_value, content_types=['text'],
                                state=RedactStudentInfoFSM.waiting_new_value)
    dp.register_message_handler(obtain_confirm, lambda x: x.text in ['Да', 'Нет', 'да', 'нет'],
                                state=RedactStudentInfoFSM.waiting_confirm)
    dp.register_message_handler(add_many_students_info, commands=['add_students_data'])
    dp.register_message_handler(get_csv_file, content_types=['document'], state=AddStudentInfoFSM.waiting_csv_file)
    dp.register_message_handler(redact_schedule, commands=['redact_schedule'])
    dp.register_message_handler(obtain_institute_name, content_types=['text'],
                                state=RedactScheduleFSM.waiting_institute_name)
    dp.register_message_handler(obtain_image_id, content_types=['photo'], state=RedactScheduleFSM.waiting_image_id)
