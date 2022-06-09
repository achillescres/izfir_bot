from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.mongo import MongoStorage


from bot.data import config

# Create bot
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Create dispatcher
try:
    storage = MongoStorage(host='localhost', port=27017)
except Exception:
    print('Failed to connect to MongoDB for FSM')
    print('Raising MemoryStorage...')
    storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)  # File end-point
