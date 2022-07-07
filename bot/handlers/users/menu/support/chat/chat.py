from loguru import logger

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.abstracts.support import AbstractTicket
from bot.keyboards.default.menu import menu_kb
from bot.states.machines import ChatFSM
from bot.utils.chat.utils import score_chat_with_message
from bot.utils.misc import remove_kb
from loader import dp

from bot.keyboards.default.chat import chat_kbs

import bot.utils.http as http


# Universal function to close_chat, closing user-side and operator-side
async def finish_chat(message: types.Message, state: FSMContext, from_user=True, with_err=False):
	if from_user:
		await remove_kb(message=message, kb=menu_kb.kb)
		
		try:
			async with state.proxy() as fsm_data_proxy:
				if 'operator_name' in fsm_data_proxy:
					fsm_data_proxy.pop('operator_name')
				operator_id = None
				if 'operator_id' in fsm_data_proxy:
					operator_id = fsm_data_proxy.pop('operator_id')
				
				await AbstractTicket.delete(
					state=state,
					ticket_id=operator_id,
					sync=False
				)
				
				if operator_id:
					await score_chat_with_message(ticket_id=operator_id, message=message)
					canceled = await http.chat.cancel(operator_id=operator_id, user_id=message.from_user.id)
					if canceled == 'err' or with_err:
						logger.warning('Error while finishing support or support!')
						canceled = await http.chat.cancel(operator_id=operator_id, user_id=message.from_user.id)
						if canceled == 'err':
							logger.warning('Erro siht second attempt to finish support!')
		except Exception as e:
			logger.error(e)
			logger.error("Can't delete ticket with AbstractTicket method")


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
