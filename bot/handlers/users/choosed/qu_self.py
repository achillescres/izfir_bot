from aiogram import types

from loader import dp
from bot.states import FSM
from bot.utils.load_qus_ans import load_qus_ans, make_qu_to_an


qus_ans_calls = load_qus_ans()
qu_to_an = make_qu_to_an(qus_ans_calls)


@dp.message_handler(text=[qu for (qu, an, call) in qus_ans_calls], state=FSM.choosed)
async def qu_ans(message: types.Message):
    await message.answer(text=qu_to_an[message.text])
