from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.misc import faculties_names


faculties_names_hashes = [(name, str(hash(name))) for name in ['Главное меню', 'Центральная приемная комиссия'] + faculties_names]
faculties_hashes = [i[1] for i in faculties_names_hashes]
hash_to_name = {_hash: name for name, _hash in faculties_names_hashes}

ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=_hash)] for name, _hash in faculties_names_hashes
    ]
)
