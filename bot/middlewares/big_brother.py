from loguru import logger

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        logger.info('[--------------------------New update!---------------------]')
        logger.info('1. Pre process Update')
        logger.info('Next point: Process Update')
    