from loguru import logger

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import text, bold

from bot.abstracts.support import AbstractTicket
from bot.keyboards.default.menu import menu_kb
from bot.states.machines import ChatFSM
from loader import dp

from bot.keyboards.default.chat import chat_kbs

from bot.states import MenuFSM
import bot.utils.http as http


# apply operator message == ChatFSM.apply_chat --> CHAT == ChatFSM.support
@dp.callback_query_handler(text=chat_kbs.Texts.start_chat_hash.value, state=MenuFSM.main)
async def start_chat(call: types.CallbackQuery, state: FSMContext):
	await call.message.answer(
		text(
			'Начался чат с оператором, чтобы отправить сообщение просто напишите его мне,',
			'чтобы завершить сеанс воспользуйтесь кнопкой, или напишите',
			bold('/start'),
		),
		reply_markup=chat_kbs.finish_chat_kb
	)
	
	await state.set_state(ChatFSM.chat)


# cancel operator message == ChatFSM.apply_chat --> MAIN MENU
@dp.callback_query_handler(text=chat_kbs.Texts.cancel_chat_hash.value, state=MenuFSM.main)
async def cancel_chat(call: types.CallbackQuery, state: FSMContext):
	await call.message.edit_reply_markup(None)
	await call.message.reply('Заявка на чат была вами отклонена')
	await state.set_state(MenuFSM.main)
	await AbstractTicket.enable(
		ticket_id=(await state.get_data())['ticket_id'],
		state=state
	)


# Universal function to close_chat, closing user-side and operator-side
async def finish_chat(message: types.Message, state: FSMContext, from_user=True, with_err=False):
	if from_user:
		operator_id = (await state.get_data()).get('operator_id')
		
		canceled = await http.chat.cancel(operator_id=operator_id, user_id=message.from_user.id)
		if canceled == 'err' or with_err:
			logger.warning('Error while finishing support or support!')
			canceled = await http.chat.cancel(operator_id=operator_id, user_id=message.from_user.id)
			if canceled == 'err':
				logger.warning('Erro siht second attempt to finish support!')
		await message.answer('Cеанс завершен', reply_markup=menu_kb.kb)
	
	# await state.finish()
	await state.set_state(MenuFSM.main)
	await AbstractTicket.delete(
		ticket_id=(await state.get_data())['ticket_id'],
		state=state
	)


# Close on keyboard close button
@dp.message_handler(text=[chat_kbs.Texts.finish_chat.value, '/start'], state=ChatFSM.chat)
async def close_chat(message: types.Message, state: FSMContext):
	await finish_chat(message, state, from_user=True, with_err=False)


# in-in-dev
@dp.message_handler(state=ChatFSM.chat, content_types=['photo'])
async def docs_photo(message):
	await message.photo[-1].download(destination_file='test.jpg')


# Send message from user
@dp.message_handler(state=ChatFSM.chat)
async def send_message(message: types.Message, state: FSMContext):
	operator_id = (await state.get_data()).get('operator_id')
	logger.info(f'Sending message to operator: {operator_id} from user: {message.from_user.id}')
	
	# If haven't operator_id in FSM
	if not operator_id:
		logger.info(f'HAVE NOT OPERATOR_ID IN FSM! CLOSING_CHAT FOR USER: {message.from_user.id}')
		await finish_chat(message, state, from_user=True, with_err=True)
		return
	
	logger.info(f'Sending message to {operator_id}')
	# Send message to site api(http library always makes 3 attempts)
	sent = await http.chat.produce_message(
		user_id=message.from_user.id,
		operator_id=operator_id,
		message=message.text
	)
	
	# If couldn't send
	if sent == 'err':
		logger.info(f"Couldn't send message to operator: {operator_id} from user: {message.from_user.id}")
		await finish_chat(message, state, from_user=True, with_err=True)
