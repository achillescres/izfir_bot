from aiogram import types
from loader import dp


@dp.message_handler(text='Ответы на частые вопросы')
async def questions(message: types.Message):
    await message.answer(f"Skoro voprosy")
