from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import qus_ans_calls


iqu_list_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=call)]
        for (text, ans, call) in qus_ans_calls
    ]
)
