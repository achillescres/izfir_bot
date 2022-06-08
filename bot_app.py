import logging

from aiogram import Dispatcher, Bot, types


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

    async def start(self, WEBHOOK_URL):
        from handlers import dp
        self.dp = dp
        await on_startup(self.dp)

        webhook_info = await self.bot.get_webhook_info()
        if webhook_info.url != WEBHOOK_URL:
            await self.bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)

        print('IzfirBot: Dispatcher loaded')

    async def shutdown(self):
        await on_shutdown(self.dp)
        await self.dp.bot.close_bot()

        logging.info('Bot shutted down!')

    async def update(self, update: dict):
        telegram_update = types.Update(**update)
        Dispatcher.set_current(self.dp)
        Bot.set_current(self.bot)
        await self.dp.process_update(telegram_update)

    @property
    def bot(self):
        return self.dp.bot
