from aiogram import types

from bot.states import FSM
from loader import dp


@dp.message_handler(state=FSM.choosed)
async def trash(message: types.Message):
    await message.reply(text='Не понимаю команды. Воспользуйтесь /help')
