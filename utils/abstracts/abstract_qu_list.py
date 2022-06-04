from aiogram import types

from keyboards.inline import iqu_list_kb


class AbstractQuList:
    text = 'Ответы на частые вопросы'
    ikb = iqu_list_kb

    @staticmethod
    def _get_message(obj: types.Message | types.CallbackQuery):
        return obj.message if isinstance(obj, types.CallbackQuery) else obj

    @staticmethod
    async def send_qu_list(obj: types.Message | types.CallbackQuery):
        await AbstractQuList._get_message(obj)\
            .answer(AbstractQuList.text, reply_markup=AbstractQuList.ikb)

    @staticmethod
    async def set_qu_list(obj: types.Message | types.CallbackQuery):
        message = AbstractQuList._get_message(obj)
        await message.edit_text(AbstractQuList.text)
        await message.edit_reply_markup(AbstractQuList.ikb)
