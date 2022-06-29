from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.abstracts import TextEnum


class Texts(TextEnum):
    chat = 'Спросить у оператора'
    active_tickets = 'Мои активные вопросы'
    answers = 'Мои ответы'
    return_to_menu = 'Главное меню'


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text) for text in Texts.values()],
    ],
    resize_keyboard=True
)