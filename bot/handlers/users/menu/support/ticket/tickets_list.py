from itertools import count

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.abstracts.support import AbstractTicket
from bot.keyboards.default.menu import menu_kb
from bot.states import MenuFSM
from loader import dp


@dp.message_handler(text=menu_kb.Texts.active_tickets.value, state=MenuFSM.main)
async def tickets_list(message: types.Message, state: FSMContext):
	await AbstractTicket.create(ticket_id='123', question_text='ШО ПО БВИ?', state=state)
	tickets: dict = await AbstractTicket.get_all(state)
	counter = count()
	next(counter)
	
	text = '\n'.join(
		f'{next(counter)}. {AbstractTicket.get_question(tickets[ticket_id])}: ' +
		f'{AbstractTicket.get_status_text(tickets[ticket_id])}\n'
		# f'Answer: {AbstractTicket.get_answer(tickets[ticket_id])}'
		for index, ticket_id in enumerate(tickets) if ticket_id if ticket_id.isnumeric()
	)
	
	await message.answer(
		f"Ваши тикеты:\n{text}"
	)
