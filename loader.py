import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from data import config


logging.basicConfig(level=logging.INFO)

# Create bot
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Create dispatcher
dp = Dispatcher(bot, storage=MemoryStorage())  # File end-point
dp.middleware.setup(LoggingMiddleware())