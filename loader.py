from aiogram import Bot, Dispatcher, types

from data import config


# Create bot
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Create dispatcher
dp = Dispatcher(bot)

