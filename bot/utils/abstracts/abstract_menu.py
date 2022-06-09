from aiogram import types

from bot.keyboards.default import main_kb
from bot.utils.abstracts.utils import get_message_from_obj


class AbstractMenu:
    @staticmethod
    async def send_menu(obj: types.Message | types.CallbackQuery):
        message = get_message_from_obj(obj)
        await message.answer('Главное меню', reply_markup=main_kb.kb)
