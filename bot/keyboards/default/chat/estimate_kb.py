from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.abstracts import TextEnum


class Texts(TextEnum):
    one_star = '1'
    two_star = '2'
    three_star = '3'
    four_star = '4'
    five_star = '5'


kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text) for text in Texts.values()],
    ],
    resize_keyboard=True
)
