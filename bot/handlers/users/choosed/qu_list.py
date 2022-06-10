from aiogram import types

from bot.keyboards.default import main_kb, qu_list_kb
from loader import dp
from bot.states import MainFSM


@dp.message_handler(text=main_kb.Texts.qus.value, state=MainFSM.choosed)
async def qus(message: types.Message | types.CallbackQuery):
    print('Qu List')

    await message.answer('Ответы на частые вопросы', reply_markup=qu_list_kb.kb)

