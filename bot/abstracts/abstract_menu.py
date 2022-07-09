from aiogram import types, Bot

from bot.keyboards.default.menu import menu_kb
from bot.abstracts.utils import get_message_from_obj


class AbstractMenu:
    @staticmethod
    async def send(obj: types.Message | types.CallbackQuery):
        message = get_message_from_obj(obj)
        await message.answer('Главное меню', reply_markup=menu_kb.kb)
    
    @staticmethod
    async def send_with_bot(user_id: str, bot: Bot):
        await bot.send_message(chat_id=user_id, text='Главное меню', reply_markup=menu_kb.kb)
