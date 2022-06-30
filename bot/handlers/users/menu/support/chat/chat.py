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
		ticket_id=(await state.get_data()).get('ticket_id'),
		state=state
	)
	

# Close on keyboard close button
@dp.message_handler(text=[chat_kbs.Texts.finish_chat.value, '/start'], state=ChatFSM.chat)
async def close_chat(message: types.Message, state: FSMContext):
	await finish_chat(message, state, from_user=True, with_err=False)


# Send message from user
@dp.message_handler(state=ChatFSM.chat)
async def send_message(message: types.Message, state: FSMContext):
	operator_id = (await state.get_data()).get('operator_id')
	logger.info(f'Sending message to operator: {operator_id} from user: {message.from_user.id}')
	
	# If haven't operator_id in FSM
	if not operator_id:
		logger.info(f'HAVE NOT operator_id IN FSM! CLOSING_CHAT FOR USER: {message.from_user.id}')
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
