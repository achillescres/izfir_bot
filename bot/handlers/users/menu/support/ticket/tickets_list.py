from itertools import count

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.abstracts import AbstractMenu
from bot.abstracts.support import AbstractTicket
from bot.keyboards.default.menu import support_kb
from bot.keyboards.inline import ticket_list_ikb
from bot.states import MenuFSM
from bot.utils.misc import remove_kb
from loader import dp


@dp.message_handler(text=support_kb.Texts.active_tickets.value, state=MenuFSM.main)
async def tickets_list(message: types.Message, state: FSMContext):
	# await AbstractTicket.create(ticket_id='1', question_text='ГОВНО?', state=state)
	# await AbstractTicket.create(ticket_id='2', question_text='ЗАЛУПА?', state=state)
	# await AbstractTicket.create(ticket_id='3', question_text='ПЕНИС?', state=state)
	# await AbstractTicket.create(ticket_id='4', question_text='ХУЙ?', state=state)
	# await AbstractTicket.create(ticket_id='5', question_text='БЛЯДИНА?', state=state)
	# await AbstractTicket.create(ticket_id='6', question_text='иди нахуй анрей?', state=state)
	tickets = await AbstractTicket.get_all(state)
	
	await remove_kb(message=message)
	
	counter = count()
	next(counter)
	
	ticket_texts = '\n'.join(
		f'{next(counter)}. {AbstractTicket.get_question(tickets[ticket_id])}'
		for index, ticket_id in enumerate(tickets) if ticket_id.isnumeric()
	)
	
	ticket_raws = tuple(
		(index + 1, str(ticket_id))
		for index, ticket_id in enumerate(tickets) if ticket_id.isnumeric()
	)
	
	ticket_ids = [
		ticket_id for ticket_id in tickets if ticket_id.isnumeric()
	]
	
	if ticket_raws:
		await message.answer(
			f"Чтобы удалить вопрос нажмите на кнопку с его номером\n{ticket_texts}",
			reply_markup=ticket_list_ikb.ikb(ticket_raws)
		)
		dp.raw_proxy.tickets = ticket_ids
	else:
		await message.answer(
			f"У нет активныхх вопросов",
		)


@dp.callback_query_handler(text=ticket_list_ikb.Texts.return_to_menu_data.value, state=MenuFSM.main)
async def return_to_main_menu(call: types.CallbackQuery):
	await AbstractMenu.send(call)
	dp.raw_proxy.tickets = []


@dp.callback_query_handler(text=dp.raw_proxy.tickets, state=MenuFSM.main)
async def ticket_delete(call: types.CallbackQuery, state: FSMContext):
	ticket_id = call.data
	await call.message.answer(
		f'Вы удалили вопрос:\n{AbstractTicket.get_question(await AbstractTicket.get_ticket(ticket_id, state))}'
	)
	await dp.bot.answer_callback_query(callback_query_id=call.id)
	await AbstractTicket.delete(state=state, ticket_id=ticket_id)
	dp.raw_proxy.tickets = []
