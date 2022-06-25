from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from bot.abstracts import AbstractMenu
from bot.states import MenuFSM
from loader import dp


@dp.message_handler(Command('start'), state='*')
async def before_start(message: types.Message, state: FSMContext):
    await AbstractMenu.send(message)
    await state.set_state(MenuFSM.main)
