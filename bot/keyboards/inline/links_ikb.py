from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.abstracts import TextEnum


def generate_link_dict(text, url):
    return {'text': text, 'url': url}


class Texts(TextEnum):
    site = generate_link_dict('Сайт центральной приемной комиссии', 'https://priem.s-vfu.ru/')
    bak = generate_link_dict('Правила приема на бакалавриат и специалитет 2022', 'https://priem.s-vfu.ru/%d0%bf%d1%80%d0%b8%d0%b5%d0%bc%d0%bd%d0%b0%d1%8f-%d0%ba%d0%b0%d0%bc%d0%bf%d0%b0%d0%bd%d0%b8%d1%8f-2022/ppbs2022/')
    mag = generate_link_dict('Правила приема на магистратуру 2022', 'https://priem.s-vfu.ru/%d0%bf%d1%80%d0%b8%d0%b5%d0%bc%d0%bd%d0%b0%d1%8f-%d0%ba%d0%b0%d0%bc%d0%bf%d0%b0%d0%bd%d0%b8%d1%8f-2022/ppmag2022/')
    asp = generate_link_dict('Правила приема на аспирантуру 2022', 'https://priem.s-vfu.ru/news/ppasp2022/')
    ordi = generate_link_dict('Правила приема на ординатуру 2022', 'https://priem.s-vfu.ru/news/ppord2022/')


ikb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(**item)] for item in Texts.values()
    ]
)
