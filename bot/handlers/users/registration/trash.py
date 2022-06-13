from aiogram import types
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold, text

from loader import dp


@dp.message_handler(state=None)
async def before_start(message: types.Message):
    await message.reply(text('Напишите', bold('/start')), parse_mode=ParseMode.MARKDOWN_V2)
