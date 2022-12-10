from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from bot.bot_run import bot
from bot.utils.admin_require_wrapper import admin_require
from bot.utils.csv_parser import csv_parser
from bot.utils.request_funcs import add_many_student_data


class AddStudentInfoFSM(StatesGroup):
    """Машина состояний - диалог добавления ин-фы о студентах."""
    waiting_csv_file = State()


@admin_require
async def add_many_students_info(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, 'Отправльте файл в формате "CSV" с информацией о студентах!')
    await AddStudentInfoFSM.next()


async def get_csv_file(message: types.Message, state: FSMContext) -> None:
    if message.document.file_name.endswith('.csv'):
        with await bot.download_file_by_id(message.document.file_id) as file:
            res = await add_many_student_data(await csv_parser(str(file.read(), 'utf-8')))
            await bot.send_message(message.from_user.id,
                                   f'Успешно добавлена информация о студентах ({res["students_added_counter"]} шт.)!')
    else:
        await bot.send_message(message.from_user.id, 'Не правильный формат файла!')
    await state.finish()


def register_add_students_data_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(add_many_students_info, commands=['add_students_data'])
    dp.register_message_handler(get_csv_file, content_types=['document'], state=AddStudentInfoFSM.waiting_csv_file)
