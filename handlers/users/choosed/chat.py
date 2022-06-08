from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import FSM
from utils.http import get_http


@dp.message_handler(text='Связаться с оператором')
async def start_chat(message: types.Message, state: FSMContext):
    await message.answer('Идёт поиск оператора...')

    # Запрос на апи для поиска опреатора
    operator_id = await get_http(f'http://127.0.0.1:8000/api/getOperator/{message.chat.id}')

    # Если нет свободного оператора
    if operator_id == "null":
        await message.answer('Извините! На данный момент все операторы заняты, либо отсутствуют.\nНапишите позже')
        return

    await state.set_state(FSM.waiting_chat)
    await state.update_data(operator_id=operator_id)
    await message.reply('Оператор нашёлся!')


# @dp.message_handler(commands=['Техподдержка'])
# async def techSupport(message: types.Message, ):
