from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


qus = [
    ['1. На какие программы осуществляется',
     'qu1'],
    ['/будет/проходит набор в бакалавриат в 2022г.?',
     'qu1']
]

iqu_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text=qu[0], callback_data=qu[1])]
        for qu in qus
    ]
)
