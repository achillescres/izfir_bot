from aiogram import types

from bot.states import MainFSM
from loader import dp


@dp.message_handler(state=MainFSM.choosed)
async def trash(message: types.Message):
    await message.reply(text='Не понимаю команды. Воспользуйтесь /help')
