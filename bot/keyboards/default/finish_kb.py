from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

finish_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/Завершить')
        ],
    ],
    resize_keyboard=True,
)
