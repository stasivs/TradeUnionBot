import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            logging.info(
                f"message: {update.message.text}, user_id: {update.message.from_user.id}"
            )

        elif update.callback_query:
            logging.info(
                f"message: прожал inline кнопку, user_id: {update.callback_query.from_user.id}"
            )

        else:
            return
