from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '5548062448:AAGoAK02eNB3aXRdEPN10hSzkpbfgGSqjUI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# class FindOperator(StatesGroup):
#     waiting_for_operator = State()
#     # waiting_for_food_size = State()

#
# async def produce(sender_id, sender, operator_id, message):
#     async with websockets.connect('ws://127.0.0.1:8000/api/chat/' + operator_id) as ws:
#         await ws.send(json.dumps({'sender_id': sender_id, 'sender': sender, 'message': message}))
#         await ws.recv()
#
#
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(message.text)

#
# @dp.message_handler(commands=['Техподдержка'])
# async def techSupport(message: types.Message, state: FSMContext):
#     await message.answer('Идёт поиск оператора...')
#     res = requests.get(
#         'http://127.0.0.1:8000/api/getOperator/' + str(message.chat.id)).text.strip('"')
#     if res != "null":
#         await state.set_state('waiting_for_chat_message')
#         await state.update_data(operator_id=res)
#         print(res)
#         await message.answer('Оператор нашёлся! Напишите свой вопрос.')
#     else:
#         await message.answer('Извините! На данный момент все операторы заняты, либо отсутствуют.\nНапишите позже')
#

# @dp.message_handler(state='waiting_for_chat_message', commands=['Завершить'])
# async def closeSupport(message: types.Message, state: FSMContext):
#     await message.answer('Вы завершили сеанс')
#     data = await state.get_data()
#     user_data = data.get('operator_id')
#     await produce(message.chat.id, 'Абитуриент', user_data, 'завершил сеанс')
#     state.set_state('')
#     # res = requests.get('http://127.0.0.1:8000/api/getOperator/')

#
# @dp.message_handler(state='waiting_for_chat_message')
# async def echo(message: types.Message, state: FSMContext):
#     print(12345)
#     data = await state.get_data()
#     user_data = data.get('operator_id')
#     print(user_data)
#     await produce(message.chat.id, message.chat.first_name + ' ' + message.chat.last_name, user_data, message.text)
#     # await message.answer(message.text)
#

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
