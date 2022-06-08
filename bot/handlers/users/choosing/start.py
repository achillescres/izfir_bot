from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from bot.keyboards.default import choose_kb
from loader import dp
from bot.states import FSM


@dp.message_handler(Command('start'), state='*')
async def start(message: types.Message, state: FSMContext):
    await message.answer('Вы на бакалавриат или на магистратуру',
                         reply_markup=choose_kb)
    await state.set_state(FSM.choosing)
