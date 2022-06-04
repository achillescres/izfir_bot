from aiogram import types

from keyboards.inline import iqu_kb
from loader import dp
from states import Fsm


@dp.message_handler(text='Частые вопросы')
async def questions(message: types.Message):
    await message.answer('Ответы на частые вопросы', reply_markup=iqu_kb)
    await Fsm.main.set()
