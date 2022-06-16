from aiogram import types
from aiogram.types import ParseMode
from aiogram.utils.markdown import text, bold


options = {'state': None}


async def handler(message: types.Message):
    await message.reply(text('Напишите ', bold('/start'), sep=''),
                        parse_mode=ParseMode.MARKDOWN_V2)
