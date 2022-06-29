from aiogram import types

from bot.keyboards.default.menu import support_kb
from bot.states import MenuFSM
from loader import dp


@dp.message_handler(text=support_kb.Texts.answers.value, state=MenuFSM.main)
async def answers(message: types.Message):
	await message.answer('Нажмите на тег: #свфуответ')
