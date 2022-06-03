from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline import iqu_kb, iqu_self_kb
from loader import dp


@dp.message_handler(text='Частые вопросы')
async def questions(message: types.Message):
    await message.answer('test', reply_markup=iqu_kb)


@dp.callback_query_handler(text='qu1')
async def question1(call: CallbackQuery):
    await call.message.answer("На три программы", reply_markup=iqu_self_kb)
