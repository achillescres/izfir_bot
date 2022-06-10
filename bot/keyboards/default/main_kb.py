from enum import Enum

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.abstracts import TextEnum


class Texts(TextEnum):
    qus = 'Частые вопросы'
    links = 'Полезные ссылки'
    chat = 'Связаться с оператором'


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text) for text in Texts.values()],
    ],
    resize_keyboard=True,
)
