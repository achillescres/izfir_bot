from aiogram import types

from bot.keyboards.default import qu_list_kb
from bot.keyboards.inline import iqu_list_kb
from bot.utils.abstracts.utils import get_message_from_obj


class AbstractQuList:
    text = 'Ответы на частые вопросы'
    kb = qu_list_kb
    ikb_returner = iqu_list_kb

    @staticmethod
    async def send_qu_list(obj: types.Message | types.CallbackQuery):
        message = get_message_from_obj(obj)
        # Questions kb
        await message.answer(AbstractQuList.text, reply_markup=AbstractQuList.kb)
