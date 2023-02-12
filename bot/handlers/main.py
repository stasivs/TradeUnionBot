from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters

from utils import keyboards, request_funcs
from bot_run import bot


async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Выход из машины состояний. """

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    check = await request_funcs.get_student_info("telegram_id", message.from_user.id)
    if check:
        await bot.send_message(message.from_user.id, 'OK',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, 'OK',
                               reply_markup=keyboards.REGISTRATION_KEYBOARD)


async def greeting(message: types.Message, state: FSMContext) -> None:
    """Отлавливает команду /start, выводит соответствующую клавиатуру."""

    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    check = await request_funcs.get_student_info("telegram_id", message.from_user.id)
    if check:
        await bot.send_message(message.from_user.id, 'Вас приветствует бот профкома!',
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id,
                               'Вас приветствует бот профкома! Вам необходимо пройти регистрацию')
        await bot.send_message(message.from_user.id,
                               'Нажимая на кнопку «Регистрация» вы даете своё согласие на обработку '
                               'персональных данных и получения важной информации, связанной с подачей '
                               'и приемом документов на материальную помощь',
                               reply_markup=keyboards.REGISTRATION_KEYBOARD)
    await message.delete()


def register_main_handlers(dp: Dispatcher) -> None:
    """Регистрация админских хендлеров."""
    dp.register_message_handler(cancel_handler, filters.Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(greeting, commands=["start"], state="*")
