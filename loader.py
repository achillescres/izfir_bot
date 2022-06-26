import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2


from data import config

# Create bot
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Create dispatcher
storage = None
try:
    storage = RedisStorage2(host='localhost', port=6379, db=0)
    # storage = MongoStorage()
except Exception as e:
    logging.info('Failed to connect to Redis')
    # logging.info('Raising MemoryStorage...')
    # storage = MemoryStorage()
    logging.error(e)
    exit(-1)

dp = Dispatcher(bot, storage=storage)  # File end-point
