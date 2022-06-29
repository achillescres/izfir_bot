from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.abstracts import TextEnum


self_text = 'Главное меню'


class Texts(TextEnum):
    qus = 'Частые вопросы'
    links = 'Полезные ссылки'
    support = 'Спросить вопрос'


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text) for text in Texts.values()],
    ],
    resize_keyboard=True
)

return_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(
        text=self_text,
    )
)
