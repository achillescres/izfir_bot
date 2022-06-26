from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.abstracts import TextEnum


# Not for iterating for kb
class Texts(TextEnum):
    start_chat = 'Начать чат'
    start_chat_hash = str(hash('Начать чат'))
    cancel_chat = 'Отклонить'
    cancel_chat_hash = str(hash('Отклонить'))
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


async def start_chat_ikb(ticket_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=Texts.start_chat.value, data=Texts.start_chat_hash.value)],
            [InlineKeyboardButton(text=Texts.cancel_chat.value, data=Texts.cancel_chat_hash.value)]
        ]
    )

finish_chat_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Texts.finish_chat.value)],
    ],
    resize_keyboard=True,
)
