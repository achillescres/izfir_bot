from aiogram import types

from loader import dp
from states import FSM
from utils.abstracts import AbstractQuList


@dp.message_handler(text='Частые вопросы', state=FSM.choosed)
async def qus(message: types.Message | types.CallbackQuery):
    print('Qu List')
    await AbstractQuList.send_qu_list(message)
