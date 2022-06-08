from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

iqu_list_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Вернуться к главному меню',
                                 callback_data='qu_list_remove')
        ]
    ]
)
