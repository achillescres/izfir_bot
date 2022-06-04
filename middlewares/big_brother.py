import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        logging.info('[--------------------------New update!---------------------]')
        logging.info('1. Pre process Update')
        logging.info('Next point: Process Update')
    