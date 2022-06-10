from aiogram import types

from loader import dp
from bot.states import MainFSM
from bot.utils.load_qus_ans import load_qus_ans, make_qu_to_an_origin


qus_ans_calls = load_qus_ans()
qu_to_an_origin = make_qu_to_an_origin(qus_ans_calls)


@dp.message_handler(text=[qu for (qu, an, call, origin) in qus_ans_calls], state=MainFSM.choosed)
async def qu_ans(message: types.Message):
    qalo = qu_to_an_origin[message.text]
    await message.delete()
    await message.answer(text=qalo['origin'])
    await message.answer('Ответ: ')
    await message.answer(text=qalo['answer'])
