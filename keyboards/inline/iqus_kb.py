from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


qus = [
    ['Question 1',
     'qu1']
]

iqu_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text=qu[0], callback_data=qu[1])]
        for qu in qus
    ]
)
