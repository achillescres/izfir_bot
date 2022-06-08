from aiogram import types

from loader import dp
from states import FSM


@dp.message_handler(state=[FSM.choosed])
async def trash_after_choosing(message: types.Message):
    await message.reply('Данной команды нет, воспользуйтесь командой /help')


@dp.message_handler(state=None)
async def trash_befort_choosing(message: types.Message):
    await message.reply('Напишите /start')
