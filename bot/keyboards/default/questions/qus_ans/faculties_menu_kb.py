from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.default.menu import menu_kb


self = 'Выберите факультет'


def get_faculties_menu_kb(questions):
    return ReplyKeyboardMarkup(
        row_width=1,
        keyboard=[[KeyboardButton(text=menu_kb.self_text)]] + [
            [KeyboardButton(text=faculty_obj['faculty']['name'])] for faculty_obj in questions
        ],
        resize_keyboard=True
    )


def get_faculty_qus_ans_ikbs(questions):
    return {faculty_obj['faculty']['name']: InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [InlineKeyboardButton(text=qu_an['qu'], callback_data=qu_an['call'])]
            for qu_an in faculty_obj['qus_ans_calls']
        ]
    ) for faculty_obj in questions}
