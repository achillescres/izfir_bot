from aiogram import types

from loader import dp


@dp.message_handler(state=None)
async def trash_befort_choosing(message: types.Message):
    await message.reply('Напишите /start')
