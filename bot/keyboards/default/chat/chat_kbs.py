from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.keyboards.abstracts import TextEnum


class Texts(TextEnum):
    finish_chat = '/Завершить сеанс'
    close_qu = '/Вернуться к главному меню'
    apply_qu = 'Подтвердить'
    discard_qu = 'Изменить'


close_qu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Texts.close_qu.value)],
    ],
    resize_keyboard=True,
)

apply_chat_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Texts.apply_qu.value),
         KeyboardButton(text=Texts.discard_qu.value),
         KeyboardButton(text=Texts.close_qu.value)]
    ],
    resize_keyboard=True,
)

finish_chat_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Texts.finish_chat.value)],
    ],
    resize_keyboard=True,
)
