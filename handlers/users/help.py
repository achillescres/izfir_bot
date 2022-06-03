from aiogram import types
from loader import dp


@dp.message_handler()
async def help(message: types.Message):
    await message.reply('Я пока тупенькаяб извини')
