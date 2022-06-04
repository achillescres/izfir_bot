from aiogram import types

from filters import IsPrivate
from keyboards.default import main_kb
from loader import dp
from states import FSM


@dp.message_handler(IsPrivate(), text='/menu', state=FSM.choosed)
async def command_start(message: types.Message):
    await message.answer('Главное меню',
                         reply_markup=main_kb)
