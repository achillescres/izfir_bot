from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode
from aiogram.utils.markdown import text, bold

from loader import dp


@dp.message_handler(Command('help'), state='*')
async def help(message: types.Message):
    await message.reply(
        text(
            "Это бот ",
            bold("ЦПК СВФУ"),
            ".\nЗдесь вы можете найти ответы на распространенные вопросы или связаться с оператором.\n\n",
            bold("Команды"),
            ":\n",
            bold("/start"),
            " — начать/сбросить работу с ботом\n",
            bold("/help"),
            " — помощь по работе с ботом\n",
            bold("/menu"),
            " — главное меню"
        ), parse_mode=ParseMode.MARKDOWN
    )
