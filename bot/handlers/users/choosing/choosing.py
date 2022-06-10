from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.keyboards.default import choose_kb
from loader import dp
from bot.states import FSM
from bot.utils.abstracts.abstract_menu import AbstractMenu


@dp.message_handler(text=choose_kb.Texts.values(), state=FSM.choosing)
async def choose(message: types.Message, state: FSMContext):
    await message.reply('Ок')

    await state.set_state(FSM.choosed)
    await state.update_data(edu_type=choose_kb.Texts(message.text).name)
    await AbstractMenu.send_menu(message)


@dp.message_handler(state=FSM.choosing)
async def invalid_choose(message: types.Message, state: FSMContext):
    await message.reply('Некорректный ответ, используйте кнопки')
