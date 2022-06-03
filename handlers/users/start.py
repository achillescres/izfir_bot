from aiogram import types

from keyboards.default import main_kb
from loader import dp


@dp.message_handler(text='/start')
async def command_start(message: types.Message):
    await message.answer('Start',
                         reply_markup=main_kb)
