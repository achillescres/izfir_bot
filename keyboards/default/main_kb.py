from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Частые вопросы'),
            KeyboardButton(text='Чат')
        ],
    ],
    resize_keyboard=True,
)
