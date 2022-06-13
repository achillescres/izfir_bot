from aiogram import types

from aiogram.dispatcher import FSMContext

from bot.keyboards.default.questions import questions_menu_kb
from bot.keyboards.default.questions.qus_ans import faculties_menu_kb
from bot.states import MenuFSM
from loader import dp


@dp.message_handler(text=questions_menu_kb.Texts.qus_ans.value, state=MenuFSM.main)
async def faculties(message: types.Message):
    await message.answer('Выберите факультет', reply_markup=faculties_menu_kb.kb)


@dp.message_handler(text=faculties_menu_kb.faculties, state=MenuFSM.main)
async def faculty_self(message: types.Message):
    await message.answer(message.text, reply_markup=faculties_menu_kb.faculty_qus_ans_ikbs[message.text])
