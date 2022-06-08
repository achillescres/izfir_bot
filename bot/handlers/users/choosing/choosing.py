from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from bot.states import FSM
from bot.utils.abstracts.abstract_menu import AbstractMenu


@dp.message_handler(state=FSM.choosing)
async def choose(message: types.Message, state: FSMContext):
    if message.text not in ['Бакалавриат', 'Магистратура']:
        await message.reply('Некорректный ответ, используйте кнопки')
        return

    await message.reply('Ок')

    await state.set_state(FSM.choosed)
    await AbstractMenu.send_menu(message)
    match message.text:
        case 'Бакалавриат':
            await state.update_data(edu_type='bak')
        case 'Магистратура':
            await state.update_data(edu_type='mag')
