from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.default.menu import menu_kb


async def get_ikb(hash_to_name: dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[[InlineKeyboardButton(text='Главное меню', callback_data=menu_kb.return_data)]] + [
            [InlineKeyboardButton(text=hash_to_name[hash], callback_data=hash)] for hash in hash_to_name
        ]
    )
