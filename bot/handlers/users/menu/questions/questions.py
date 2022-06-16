from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.abstracts.abstract_questions_menu import AbstractQuestionsMenu
from bot.keyboards.default.menu import menu_kb
from bot.states import MenuFSM
from loader import dp


@dp.message_handler(text=menu_kb.Texts.qus.value, state=MenuFSM.main)
async def questions(message: types.Message):
    await AbstractQuestionsMenu.send_questions_menu(message)
