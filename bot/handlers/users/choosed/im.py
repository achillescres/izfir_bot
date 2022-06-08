from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from bot.states import FSM


@dp.message_handler(text='im', state=FSM.choosed)
async def im(message: types.Message, state: FSMContext):
    print(await state.get_data('educztion_type'))
    await message.reply(text=(await state.get_data('educztion_type')).get('edu_type'))


@dp.message_handler(text='im', state='*')
async def im(message: types.Message, state: FSMContext):
    print(edu_type := (await state.get_data()).get('edu_type'))
    await message.reply(text=f'Not choosed: {edu_type}')
