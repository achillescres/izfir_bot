from aiogram import types

from bot.abstracts.utils import get_message_from_obj
from bot.keyboards.default.menu import menu_kb
from bot.keyboards.default.questions import questions_menu_kb


class AbstractQuestionsMenu:
    @staticmethod
    async def send_questions_menu(obj: types.Message | types.CallbackQuery):
        message = get_message_from_obj(obj)
        await message.answer(menu_kb.Texts.qus.value, reply_markup=questions_menu_kb.kb)
