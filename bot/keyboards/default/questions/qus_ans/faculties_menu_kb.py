from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.default.menu import menu_kb


class QuAn:
    def __init__(self, qu: str, an: str, call: str):
        self.qu = qu
        self.an = an
        self.call = call


faculties = ["АВТОДОРОЖНЫЙ ФАКУЛЬТЕТ", "ГОРНЫЙ ИНСТИТУТ", "ГЕОЛОГОРАЗВЕДОЧНЫЙ ФАКУЛЬТЕТ", "ИНСТИТУТ ЕСТЕСТВЕННЫХ НАУК", "ИНСТИТУТ ЗАРУБЕЖНОЙ ФИЛОЛОГИИ И РЕГИОНОВЕДЕНИЯ", "ИНСТИТУТ МАТЕМАТИКИ И ИНФОРМАТИКИ", "ИНСТИТУТ ПСИХОЛОГИИ", "ИНЖЕНЕРНО-ТЕХНИЧЕСКИЙ ИНСТИТУТ", "ИСТОРИЧЕСКИЙ ФАКУЛЬТЕТ", "ИНСТИТУТ ФИЗИЧЕСКОЙ КУЛЬТУРЫ И СПОРТА", "ИНСТИТУТ ЯЗЫКОВ И КУЛЬТУРЫ НАРОДОВ СЕВЕРО-ВОСТОКА РОССИЙСКОЙ ФЕДЕРАЦИИ", "МЕДИЦИНСКИЙ ИНСТИТУТ", "ПЕДАГОГИЧЕСКИЙ ИНСТИТУТ", "ФИЛОЛОГИЧЕСКИЙ ФАКУЛЬТЕТ", "ФИЗИКО-ТЕХНИЧЕСКИЙ ИНСТИТУТ", "ФИНАНСОВО-ЭКОНОМИЧЕСКИЙ ИНСТИТУТ", "ЮРИДИЧЕСКИЙ ФАКУЛЬТЕТ", "ПОЛИТЕХНИЧЕСКИЙ ИНСТИТУТ (ФИЛИАЛ) СВФУ В Г. МИРНОМ", "ТЕХНИЧЕСКИЙ ИНСТИТУТ (ФИЛИАЛ) СВФУ В Г. НЕРЮНГРИ", "ЧУКОТСКИЙ ФИЛИАЛ СВФУ В Г. АНАДЫРЕ"]


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
            [InlineKeyboardButton(text=qu_an['qu'], callback_data=qu_an['call'])] for qu_an in faculty_obj['qus_ans_calls']
        ]
    ) for faculty_obj in questions}
