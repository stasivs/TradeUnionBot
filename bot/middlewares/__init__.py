import logging

from bot_init import dp
from .message_logging import LoggingMiddleware

if __name__ == 'middlewares':
    logging.basicConfig(level=logging.INFO, filemode="w", format="%(name)s %(asctime)s %(levelname)s %(message)s")

    dp.middleware.setup(LoggingMiddleware())
