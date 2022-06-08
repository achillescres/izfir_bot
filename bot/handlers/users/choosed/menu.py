from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from bot.states import FSM
from bot.utils.abstracts.abstract_menu import AbstractMenu


@dp.message_handler(Command('menu'), state=FSM.choosed)
@dp.message_handler(text='Главное меню', state=FSM.choosed)
async def menu(message: types.Message):
    await AbstractMenu.send_menu(message)
