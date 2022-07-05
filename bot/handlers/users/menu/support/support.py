from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.keyboards.default.menu import menu_kb, support_kb
from bot.states import MenuFSM
from loader import dp


# FROM MAIN MENU -> SUPPORT MENU == MenuFSM.main

# @dp.message_handler(text=menu_kb.Texts.support.value, state=MenuFSM.main)
# async def support_menu(message: types.Message, state: FSMContext):
# 	await message.answer(menu_kb.Texts.support.value, reply_markup=support_kb.kb)
