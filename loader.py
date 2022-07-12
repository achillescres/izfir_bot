import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from bot.abstracts import DataProxyStorage
from bot.middlewares.antiflood import ThrottlingMiddleware
from bot.states import MenuFSM
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
    logger.error('Failed to connect to Redis')
    # logger.info('Raising MemoryStorage...')

    logger.error(e)
    exit(-1)


class MyDp(Dispatcher):
    def __init__(self, *args, **kwargs):
        self.data_proxy = DataProxyStorage()
        
        super().__init__(*args, **kwargs)


dp = MyDp(bot, storage=storage)

asyncio.run(dp.data_proxy.init(AsyncIOMotorClient("mongodb://localhost:27017").izfir.qus_ans_calls))

dp.middleware.setup(ThrottlingMiddleware())
