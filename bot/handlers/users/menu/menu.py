from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from bot.keyboards.default.menu import menu_kb
from loader import dp
from bot.states import MenuFSM
from bot.abstracts import AbstractMenu


@dp.callback_query_handler(text='return_main_kb', state=MenuFSM.main)
async def return_main_kb(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await AbstractMenu.send(call.message)
    await state.set_state(MenuFSM.main)


@dp.message_handler(Command('menu'), state=MenuFSM.main)
@dp.message_handler(text=menu_kb.self_text, state=[MenuFSM.main])
async def menu(message: types.Message):
    await AbstractMenu.send(message)
