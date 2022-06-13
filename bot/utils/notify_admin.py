import logging

from aiogram import Dispatcher

from data.config import bot_admins


async def on_startup_notify(dp: Dispatcher):
    for admin in bot_admins:
        try:
            text = 'Bot started MY overlord'
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as exc:
            logging.exception(exc)
