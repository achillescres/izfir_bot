from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.abstracts import TextEnum


class Texts(TextEnum):
    start = 'Начать чат'
    cancel = 'Отменить'


kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=text) for text in Texts.texts()
        ]
    ],
    resize_keyboard=True,
)
