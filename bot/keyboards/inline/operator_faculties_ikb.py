from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.misc import faculties_names


hash_to_name = {str(hash(name)): name
                for name in ['Главное меню', 'ЦЕНТРАЛЬНАЯ ПРИЕМНАЯ КОМИССИЯ'] + [faculty_name for faculty_name in faculties_names]}


hashes = tuple(hash_to_name.keys())

ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text=hash_to_name[hash], callback_data=hash)] for hash in hash_to_name
    ]
)
