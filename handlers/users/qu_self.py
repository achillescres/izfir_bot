from aiogram import types
from loader import dp


@dp.callback_query_handler(text='qu1')
async def qu1_ans(query: types.CallbackQuery):
    await query.message.answer('Ans for 1 qu')
