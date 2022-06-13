from aiogram import types
from aiogram.types import ParseMode
from aiogram.utils.markdown import text, bold

from loader import dp


@dp.message_handler(text='/help', state='*')
async def help(message: types.Message):
    await message.reply(
        text(
            "Это бот ",
            bold("цпк ИЗФиР СВФУ"),
            ".\nЗдесь вы можете найти ответы на распространенные вопросы или связаться с оператором.\n\n",
            bold("Команды"),
            ":\n",
            bold("/start"),
            " — начать/сбросить работу с ботом\n",
            bold("/help"),
            " — помощь по работе с ботом\n",
            bold("/main"),
            " — главное меню"
        ), parse_mode=ParseMode.MARKDOWN
    )
