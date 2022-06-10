from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.abstracts import TextEnum


class Texts(TextEnum):
    qus = 'Ответы на частые вопросы'
    nlp_qus = 'Сформулировать вопрос'
    links = 'Полезные ссылки'
    chat = 'Связаться с оператором'


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text) for text in Texts.values()],
    ],
    resize_keyboard=True,
)

return_ikb = InlineKeyboardMarkup().add(InlineKeyboardButton(
            text='Вернуться к главному меню',
            callback_data='return_main_kb'
        ))
