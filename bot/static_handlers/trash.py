from aiogram import types


async def trash(message: types.Message):
    await message.reply(text='Не понимаю команды. Воспользуйтесь /help')
