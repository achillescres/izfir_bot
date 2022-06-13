from aiogram import types

from bot.states import MenuFSM
from loader import dp


@dp.message_handler(state=MenuFSM.main)
async def trash(message: types.Message):
    await message.reply(text='Не понимаю команды. Воспользуйтесь /help')
