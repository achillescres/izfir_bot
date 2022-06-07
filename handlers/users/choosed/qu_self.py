from aiogram import types

from keyboards.inline import iqu_self_kb
from loader import dp, qus_ans_calls, calls_to_ans
from states import FSM


@dp.callback_query_handler(text=[call for (qu, an, call) in qus_ans_calls], state=FSM.choosed)
async def qu_ans(query: types.CallbackQuery):
    print(query.data)
    await query.message.edit_text(calls_to_ans[query.data])
    await query.message.edit_reply_markup(iqu_self_kb)
