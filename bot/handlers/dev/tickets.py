from itertools import count

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from bot.abstracts.support import AbstractTicket
from loader import dp


@dp.message_handler(Command('tickets'), state='*')
async def tickets(message: types.Message, state: FSMContext):
	await AbstractTicket.create(ticket_id='123', question_text='ШО ПО БВИ?', state=state)
	tickets: dict = await AbstractTicket.get_all(state)
	counter = count()
	next(counter)
	
	text = '\n'.join(
		f'{next(counter)}. {AbstractTicket.get_question(tickets[ticket_id])}: {AbstractTicket.get_status_text(tickets[ticket_id])}\nAnswer: {AbstractTicket.get_answer(tickets[ticket_id])}'
		for index, ticket_id in enumerate(tickets) if ticket_id if ticket_id.isnumeric()
	)
	
	await message.answer(
		f"Ваши тикеты:\n{text}"
	)
