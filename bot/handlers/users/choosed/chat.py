from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

from bot.states import FSM
from bot.keyboards.default import finish_kb

from bot.utils.http import get_http
from bot.utils.http import produce


@dp.message_handler(state=FSM.choosed, text='Связаться с оператором')
async def start_chat(message: types.Message, state: FSMContext):
    await message.answer('Идёт поиск оператора...')

    # Запрос на апи для поиска оператора
    operator_id = (await get_http(f'http://127.0.0.1:8000/api/getOperator/{message.chat.id}')).strip('"')
    print(operator_id)
    # Если нет свободного оператора
    if operator_id == "null":
        await message.answer('Извините! На данный момент все операторы заняты, либо отсутствуют.\nНапишите позже')
        return

    await state.set_state(FSM.chat)
    await state.update_data(operator_id=operator_id)
    await message.reply('Оператор нашёлся!', reply_markup=finish_kb)


@dp.message_handler(state=FSM.chat, commands=['Завершить'])
async def close_support(message: types.Message, state: FSMContext):
    await message.answer('Вы завершили сеанс')
    data = await state.get_data()
    operator_id = data.get('operator_id')
    await produce(message.chat.id, 'Абитуриент', operator_id, '/Завершить')
    await state.finish()
    await state.update_data(operator_id='')


@dp.message_handler(state=FSM.chat)
async def send_support(message: types.Message, state: FSMContext):
    data = await state.get_data()
    operator_id = data.get('operator_id')
    await produce(message.chat.id, f"{message.chat.first_name} {message.chat.last_name}", operator_id, message.text)
