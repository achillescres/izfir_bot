from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from bot.states import MainFSM, NlpFSM
from bot.utils.abstracts.abstract_menu import AbstractMenu


@dp.callback_query_handler(text='return_main_kb',
                           state=[MainFSM.choosed, *NlpFSM.all_states])
async def return_main_kb(call: types.CallbackQuery, state: FSMContext):
    print('FAASHIGDUYIASHOJDHGA')
    await AbstractMenu.send_menu(call.message)
    await state.set_state(MainFSM.choosed)


@dp.message_handler(Command('menu'), state=MainFSM.choosed)
@dp.message_handler(text='Главное меню', state=MainFSM.choosed)
async def menu(message: types.Message):
    await AbstractMenu.send_menu(message)

