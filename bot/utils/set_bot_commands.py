from aiogram import Dispatcher, types


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Начать работу с ботом'),
        types.BotCommand('help', 'Нужна помощь?'),
        types.BotCommand('menu', 'Главное меню')
    ])
