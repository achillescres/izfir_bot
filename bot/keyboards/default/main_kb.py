from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Частые вопросы'),
            KeyboardButton(text='Связаться с оператором')
        ],
    ],
    resize_keyboard=True,
)
