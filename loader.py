from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from loguru import logger

from data import config


logger.add('debug.log', format='{time} {level} {message}',
           level='DEBUG', rotation='5 MB', compression='tar')

# Create bot
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Create dispatcher
storage = None
try:
    storage = RedisStorage2(host='localhost', port=6379, db=0)
    # storage = MongoStorage()
except Exception as e:
    logger.info('Failed to connect to Redis')
    logger.info('Raising MemoryStorage...')
    storage = MemoryStorage()
    # logger.error(e)
    # exit(-1)

dp = Dispatcher(bot, storage=storage)


class Proxy:
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__.get(item)


dp.raw_proxy = Proxy()
