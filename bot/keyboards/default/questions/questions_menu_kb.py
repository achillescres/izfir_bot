from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.abstracts import TextEnum
from bot.keyboards.default.menu import menu_kb


class Texts(TextEnum):
    qus_ans = 'Частые вопросы'
    nlp = 'Спросить у бота'
    menu = menu_kb.self_text


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text) for text in Texts.values()],
    ],
    resize_keyboard=True
)
