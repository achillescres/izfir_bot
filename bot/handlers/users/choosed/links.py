from aiogram import types

from bot.keyboards.default import main_kb
from bot.keyboards.inline import links_ikb
from bot.states import MainFSM
from loader import dp


@dp.message_handler(text=main_kb.Texts.links.value, state=MainFSM.choosed)
async def links(message: types.Message):
    await message.delete()
    await message.answer('Полезные ссылки', reply_markup=links_ikb.kb)
