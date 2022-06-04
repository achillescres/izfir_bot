from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import main_kb
from loader import dp
from states import FSM


@dp.message_handler(state=FSM.choosing)
async def choose(message: types.Message, state: FSMContext):
    if message.text not in ['Бакалавриат', 'Магистратура']:
        await message.reply('Некорректный ответ, используйте кнопки')
        return

    await message.reply('Ок')
    await message.answer('Главное меню',
                         reply_markup=main_kb)

    await state.set_state(FSM.choosed)
    match message.text:
        case 'Бакалавриат':
            await state.update_data(education_type='bak')
        case 'Магистратура':
            await state.update_data(education_type='mag')
