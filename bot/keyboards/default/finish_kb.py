from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.abstracts import TextEnum


class Texts(TextEnum):
    cancel = '/Завершить сеанс'


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text) for text in Texts.texts()],
    ],
    resize_keyboard=True,
)
