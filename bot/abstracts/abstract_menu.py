from aiogram import types

from bot.keyboards.default.menu import menu_kb
from bot.abstracts.utils import get_message_from_obj


class AbstractMenu:
    @staticmethod
    async def send_menu(obj: types.Message | types.CallbackQuery):
        message = get_message_from_obj(obj)
        await message.answer('Главное меню', reply_markup=menu_kb.kb)
