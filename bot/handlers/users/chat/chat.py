from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

from bot.keyboards.default import main_kb
from bot.keyboards.default import finish_kb

from bot.states import FSM
import bot.utils.http as http


@dp.message_handler(text=main_kb.Texts.chat.value, state=FSM.choosed)
async def start_chat(message: types.Message, state: FSMContext):
    await state.set_state(FSM.waiting_chat)
    await message.answer('Идёт поиск оператора...')

    # Запрос на апи для поиска оператора
    operator_id = (await http.get(f'http://127.0.0.1:8000/api/getOperator/{message.chat.id}')).strip('"')
    print(operator_id)
    # Если нет свободного оператора
    if operator_id == "null":
        await message.answer('Извините! На данный момент все операторы заняты, либо отсутствуют.\nНапишите позже')
        await state.set_state(FSM.choosed)
        return

    await state.set_state(FSM.chat)
    await state.update_data(operator_id=operator_id)
    await message.reply('Оператор нашёлся!', reply_markup=finish_kb.kb)


async def close_chat(message: types.Message, state: FSMContext, from_user=True, err=False):
    if from_user:
        operator_id = (await state.get_data()).get('operator_id')

        canceled = await http.chat.cancel(operator_id=operator_id, user_id=message.from_user.id)
        if canceled == 'err' or err:
            await message.answer('Наблюдаются проблемы с подключением к операторам')

    await state.update_data(operator_id=None)
    await state.set_state(FSM.choosed)
    await message.answer('Cеанс завершен', reply_markup=main_kb.kb)


@dp.message_handler(text=finish_kb.Texts.cancel.value, state=FSM.chat)
async def close_support(message: types.Message, state: FSMContext):
    await close_chat(message, state, from_user=True)


# Send message from user
@dp.message_handler(state=FSM.chat)
async def send_support(message: types.Message, state: FSMContext):
    operator_id = (await state.get_data()).get('operator_id')
    print(f'send_support(): operator_id={operator_id}')
    # If haven't operator_id than error
    if not operator_id:
        await close_chat(message, state, from_user=True)
        return

    # Send message to site api
    sent = await http.chat.produce_message(
        user_id=message.from_user.id,
        operator_id=operator_id,
        message=message.text
    )

    print(f'send_support(): sent={sent}')
    # If couldn't send
    if sent == 'err':
        await close_chat(message, state, from_user=True, err=True)
