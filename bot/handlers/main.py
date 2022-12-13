from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters

from utils import keyboards
from bot_run import bot


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Выход из машины состояний."""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    await bot.send_message(message.from_user.id, 'OK', reply_markup=await keyboards.keyboard_choice(message.from_user.id))


async def greeting(message: types.Message) -> None:
    """Отлавливает команду /start, выводит соответствующую клавиатуру."""
    await bot.send_message(message.from_user.id, "Вас приветствует бот профкома!",
                           reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    await message.delete()


def register_main_handlers(dp: Dispatcher) -> None:
    """Регистрация админских хендлеров."""
    dp.register_message_handler(cancel_handler, filters.Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(greeting, commands=["start"], state="*")
