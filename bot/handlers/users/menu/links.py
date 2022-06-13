from aiogram import types

from bot.keyboards.default.menu import menu_kb
from bot.keyboards.inline import links_ikb
from bot.states import MenuFSM
from loader import dp


@dp.message_handler(text=menu_kb.Texts.links.value, state=MenuFSM.main)
async def links(message: types.Message):
    # await message.delete()
    await message.answer('Полезные ссылки', reply_markup=links_ikb.ikb)
