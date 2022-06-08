from aiogram import Dispatcher, types


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Бакалавриат или магистратура'),
        types.BotCommand('help', 'Нужна помощь?'),
        types.BotCommand('menu', 'Главное меню')
    ])
