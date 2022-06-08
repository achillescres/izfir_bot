import logging

from aiogram import Dispatcher, Bot
from aiogram.utils.executor import start_webhook


async def on_startup(dp: Dispatcher):
    from utils.notify_admin import on_startup_notify
    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    print('Bot started')


async def on_shutdown(dp: Dispatcher):
    logging.warning('Shutting down!..')

    await dp.bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.info('Bot shut down! Bye!')


class IzfirBot:
    dp = None

    def load_dp(self):
        from handlers import dp
        self.dp = dp

        logging.info('IzfirBot: Dispatcher loaded')

    @property
    def bot(self):
        return self.dp.bot