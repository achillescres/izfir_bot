from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.abstracts import TextEnum


class Texts(TextEnum):
    apply = 'Уверен'
    cancel = 'Изменить вопрос'


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text) for text in Texts.values()],
    ],
    resize_keyboard=True,
)
