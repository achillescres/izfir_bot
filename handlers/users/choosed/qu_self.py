from aiogram import types

from keyboards.inline import iqu_self_kb
from loader import dp
from states import FSM


@dp.callback_query_handler(text='qu1', state=FSM.choosed)
async def qu1_ans(query: types.CallbackQuery):
    print('Qu1')
    await query.message.edit_text('Ans for 1 qu')
    await query.message.edit_reply_markup(iqu_self_kb)
