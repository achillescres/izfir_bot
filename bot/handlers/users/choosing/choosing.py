from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.keyboards.default import choose_kb
from loader import dp
from bot.states import MainFSM
from bot.utils.abstracts.abstract_menu import AbstractMenu


@dp.message_handler(text=choose_kb.Texts.values(), state=MainFSM.choosing)
async def choose(message: types.Message, state: FSMContext):
    await message.reply('Ок')

    await state.set_state(MainFSM.choosed)
    await state.update_data(edu_type=choose_kb.Texts(message.text).name)
    await AbstractMenu.send_menu(message)


@dp.message_handler(state=MainFSM.choosing)
async def invalid_choose(message: types.Message, state: FSMContext):
    await message.reply('Некорректный ответ, используйте кнопки')
