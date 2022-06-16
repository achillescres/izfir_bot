from aiogram import types

from bot.abstracts.utils import get_message_from_obj
from bot.keyboards.default.questions.qus_ans import faculties_menu_kb


class AbstractFacultiesList:
    @staticmethod
    async def send(obj: types.Message | types.CallbackQuery):
        message = get_message_from_obj(obj)
        await message.answer(faculties_menu_kb.self, reply_markup=faculties_menu_kb.kb)
