from aiogram import types


options = {'state': '*'}


async def handler(message: types.Message):
    await message.reply('Не понимаю команды')
