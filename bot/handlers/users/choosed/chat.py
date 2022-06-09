from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.keyboards.default import apply_chat_kb, main_kb
from loader import dp
from bot.states import FSM
from bot.utils.http import get_http


@dp.message_handler(text=main_kb.Texts.chat.value, state=FSM.choosed)
async def start_chat(message: types.Message, state: FSMContext):
    await state.set_state(FSM.waiting_chat)
    await message.answer('Идёт поиск оператора...')

    # Запрос на апи для поиска опреатора
    operator_id = await get_http(f'http://127.0.0.1:8000/api/getOperator/{message.chat.id}')

    operator_id = '1'
    # Если нет свободного оператора
    if operator_id == "null":
        await message.answer('Извините! На данный момент все операторы заняты, либо отсутствуют.\nНапишите позже')
        await state.set_state(FSM.choosed)
        return

    await state.update_data(operator_id=operator_id)
    await message.reply(
        'Оператор нашёлся! Начать чат?',
        reply_markup=apply_chat_kb.kb
    )


@dp.message_handler(text=apply_chat_kb.Texts.start.value, state=FSM.waiting_chat)
async def start_chat(message: types.Message, state: FSMContext):
    connecting_message = await message.reply('Подключение...')

    connection = False #await connect()
    if not connection:
        await connecting_message.edit_text('Не удалось подключиться. Проверьте связь и попробуйте снова.')
        await state.set_state(FSM.choosed)
        return

    await connecting_message.edit_text('Оператор подключен. Пишите.')
    await state.set_state(FSM.chat)


@dp.message_handler(text=apply_chat_kb.Texts.cancel.value, state=FSM.waiting_chat)
async def cancel_chat(message: types.Message, state: FSMContext):
    await message.reply('Чат завершен', reply_markup=main_kb.kb)
    await state.set_state(FSM.choosed)


@dp.message_handler(state=FSM.chat)
async def chat(message: types.Message, state: FSMContext):
    pass
