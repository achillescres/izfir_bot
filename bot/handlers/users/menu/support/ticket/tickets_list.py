from itertools import count

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from loguru import logger

from bot.abstracts import AbstractMenu
from bot.abstracts.support import AbstractTicket
from bot.keyboards.default.menu import support_kb
from bot.keyboards.inline import ticket_list_ikb
from bot.states import MenuFSM
from bot.utils.misc import remove_kb
from loader import dp


def is_ticket(key: str) -> bool:
	return key.startswith('ticket_')


# @dp.message_handler(text=support_kb.Texts.active_tickets.value, state=MenuFSM.main)
# async def tickets_list(message: types.Message, state: FSMContext):
# 	# await AbstractTicket.create(ticket_id='1', question_text='1?', state=state)
# 	# await AbstractTicket.create(ticket_id='2', question_text='2?', state=state)
# 	# await AbstractTicket.create(ticket_id='3', question_text='3?', state=state)
# 	# await AbstractTicket.create(ticket_id='4', question_text='4?', state=state)
# 	# await AbstractTicket.create(ticket_id='5', question_text='5?', state=state)
# 	# await AbstractTicket.create(ticket_id='6', question_text='6?', state=state)
# 	fsm_data = await AbstractTicket.get_all(state)
# 	ticket_ids = [
# 		ticket_id for ticket_id in fsm_data if is_ticket(ticket_id)
# 	]
# 	await remove_kb(message=message)
#
# 	counter = count()
# 	next(counter)
#
# 	ticket_texts = '\n'.join(
# 		f'{next(counter)}. {AbstractTicket.get_question(fsm_data[ticket_id])}'
# 		for index, ticket_id in enumerate(fsm_data) if is_ticket(ticket_id)
# 	)
#
# 	ticket_raws = tuple(
# 		(index + 1, str(ticket_id))
# 		for index, ticket_id in enumerate(fsm_data) if is_ticket(ticket_id)
# 	)
#
# 	ticket_ids = [
# 		ticket_id for ticket_id in fsm_data if is_ticket(ticket_id)
# 	]
#
# 	if ticket_raws:
# 		await message.answer(
# 			f"Чтобы удалить вопрос нажмите на кнопку с его номером\n{ticket_texts}",
# 			reply_markup=ticket_list_ikb.ikb(ticket_raws)
# 		)
# 	else:
# 		await message.answer(
# 			f"У вас нет активных вопросов",
# 		)


@dp.callback_query_handler(text=ticket_list_ikb.Texts.return_to_menu_data.value, state=MenuFSM.main)
async def return_to_main_menu(call: types.CallbackQuery):
	await AbstractMenu.send(call)


@dp.callback_query_handler(Text(startswith='ticket_'), state=MenuFSM.main)
async def ticket_delete(call: types.CallbackQuery, state: FSMContext):
	try:
		ticket_id = call.data
		logger.info(f'Deleting ticket {ticket_id}')
		await call.message.answer(
			f'Вы удалили вопрос:\n{AbstractTicket.get_question(await AbstractTicket.get_ticket(ticket_id, state))}'
		)
		await dp.bot.answer_callback_query(callback_query_id=call.id)
		await AbstractTicket.delete(state=state, ticket_id=ticket_id)
	except KeyError:
		logger.warning('Trying delete an already deleted ticket')
		await dp.bot.answer_callback_query(callback_query_id=call.id)
	except Exception as e:
		await dp.bot.answer_callback_query(callback_query_id=call.id)
		logger.error(e)
		logger.error("Can't delete ticket!")
