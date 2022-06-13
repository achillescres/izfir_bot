from aiogram import types

from bot.keyboards.default.questions import qu_list_kb
from bot.abstracts.utils import get_message_from_obj


class AbstractQuList:
    text = 'Ответы на частые вопросы'
    kb = qu_list_kb

    @staticmethod
    async def send_qu_list(obj: types.Message | types.CallbackQuery):
        message = get_message_from_obj(obj)
        # Questions kb
        await message.answer(AbstractQuList.text, reply_markup=AbstractQuList.kb)
