from aiogram import Dispatcher


# Doing stuff for setup bot, log and notify admins
async def on_startup(dp: Dispatcher):
    from utils.notify_admin import on_startup_notify
    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    print('Bot started')


if __name__ == '__main__':
    # Starting bot
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup,
                           skip_updates=True)
