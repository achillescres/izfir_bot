from aiogram import types
from loader import dp


@dp.message_handler(text='/help', state='*')
async def help(message: types.Message):
    await message.reply('Helping message')
