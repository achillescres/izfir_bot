from aiogram import types
from aiogram.utils.emoji import emojize

from keyboards.default import qu_list_kb
from keyboards.inline import iqu_list_kb
from utils.abstracts.utils import get_message_from_obj


class AbstractQuList:
    text = 'Ответы на частые вопросы'
    kb = qu_list_kb
    ikb_returner = iqu_list_kb

    @staticmethod
    async def send_qu_list(obj: types.Message | types.CallbackQuery):
        message = get_message_from_obj(obj)
        # Questions kb
        print(await message.answer(AbstractQuList.text, reply_markup=AbstractQuList.kb))