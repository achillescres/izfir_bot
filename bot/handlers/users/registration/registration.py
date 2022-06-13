from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from bot.abstracts.abstract_menu import AbstractMenu
from bot.keyboards.default import reg_kb
from bot.states.machines import RegFSM, MenuFSM
from loader import dp


@dp.message_handler(Command('start'), state='*')
async def start(message: types.Message, state: FSMContext):
    print('Reg start')
    await message.answer('Вы на бакалавриат или на магистратуру',
                         reply_markup=reg_kb.kb)
    await state.set_state(RegFSM.education_type)


# BAK OR MAG registration step
# Answers that equals to reg_kb buttons
@dp.message_handler(text=reg_kb.Texts.values(), state=RegFSM.education_type)
async def reg_education_type(message: types.Message, state: FSMContext):
    await AbstractMenu.send_menu(message)
    await state.set_state(MenuFSM.main)
    await state.update_data(education_type=reg_kb.Texts(message.text))
    await state.update_data(operator_id=None)


# All other answers
@dp.message_handler(state=RegFSM.education_type)
async def reg_education_type(message: types.Message):
    await message.reply(text='Некорректный ответ, используйте кнопки')
