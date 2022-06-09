from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.abstracts import TextEnum


class Texts(TextEnum):  # names is also callback_data
    bak = 'Бакалавриат'
    mag = 'Магистратура'


kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=text) for text in Texts.texts()
        ],
    ],
    resize_keyboard=True,
)
