from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command('tickets'), state='*')
async def tickets(message: types.Message, state: FSMContext):
	await message.answer(str([t for t in (await state.get_data()) if t.startswith('ticket_')]))


@dp.message_handler(Command('data'), state='*')
async def data(message: types.Message, state: FSMContext):
	await message.answer(str(await state.get_data()))


@dp.message_handler(Command('clear'), state='*')
async def clear(message: types.Message, state: FSMContext):
	await state.finish()
