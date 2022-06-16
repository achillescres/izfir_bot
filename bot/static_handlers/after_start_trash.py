from aiogram import types
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold, text

from bot.states import MenuFSM


options = {
    'state': MenuFSM.main
}


async def handler(message: types.Message):
    await message.reply(
        text('Такой команды нет, пользуйтесь кнопками. Справка по боту ', bold('/help'), sep=''),
        parse_mode=ParseMode.MARKDOWN_V2
    )
