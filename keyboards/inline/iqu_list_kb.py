from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db_utils.get_qus_ans import get_qus_ans


iqu_list_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=cb_data)]
        for (text, ans, cb_data) in get_qus_ans()
    ]
)
