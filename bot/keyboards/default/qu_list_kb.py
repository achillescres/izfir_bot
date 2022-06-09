from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.utils.load_qus_ans import load_qus_ans


kb = ReplyKeyboardMarkup(
    row_width=1,
    keyboard=[[KeyboardButton(text='Главное меню')]] + [
        [KeyboardButton(text=text, callback_data=call)]
        for (text, ans, call) in load_qus_ans()
    ],
    resize_keyboard=True
)
