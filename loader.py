from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from loguru import logger

from data import config


logger.add('debug.log', format='{time} {level} {message}',
           level='DEBUG', rotation='10 MB', compression='tar')

# Create bot
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Create dispatcher
storage = None
try:
    # storage = MemoryStorage()
    storage = RedisStorage2(host='localhost', port=6379, db=1)
    # storage = MongoStorage()
except Exception as e:
    logger.info('Failed to connect to Redis')
    logger.info('Raising MemoryStorage...')

    # logger.error(e)
    # exit(-1)

dp = Dispatcher(bot, storage=storage)
