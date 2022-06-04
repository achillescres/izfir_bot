from aiogram import types

from loader import dp
from states import FSM


@dp.message_handler(state=[FSM.choosed])
async def trash(message: types.Message):
    await message.reply('Я пока тупенькаяб извини')
