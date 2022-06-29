from enum import Enum

from aiogram.dispatcher import FSMContext
from loguru import logger


class Status(Enum):
	wait_operator = 0
	wait_user = 1
	active = 2


class AbstractTicket:
	Status = Status
	
	status_to_text = {
		0: 'Ожидание оператора',
		1: 'Ождиание пользователя',
		2: 'Общение'
	}
	
	class Schema:
		status: Status = 'status'  # keys for dict
		question: str = 'question'
		answer: str = 'answer'
		
	@classmethod
	def new(cls, question: str, status: int = 0, answer: str | None = None) -> dict:
		return {cls.Schema.status: status, cls.Schema.question: question, cls.Schema.answer: answer}
	
	@classmethod
	async def get_ticket(cls, ticket_id: str, state: FSMContext):
		return (await state.get_data())[ticket_id]
	
	@classmethod
	def get_status(cls, ticket: dict) -> int:
		return ticket.get(cls.Schema.status)

	@classmethod
	def get_status_text(cls, ticket: dict) -> str:
		return AbstractTicket.status_to_text.get(cls.get_status(ticket))
	
	@classmethod
	def get_question(cls, ticket: dict) -> str:
		return ticket[cls.Schema.question]
	
	@classmethod
	def get_answer(cls, ticket: dict) -> str:
		return ticket[cls.Schema.answer]
	
	@classmethod
	async def create(cls, ticket_id: str, question_text: str, state: FSMContext) -> bool:
		try:
			async with state.proxy() as fsm_data_proxy:
				fsm_data_proxy[ticket_id] = cls.new(question_text)
		except Exception as e:
			logger.error(e)
			logger.error('Can\'t create a support')
			return False
	
	@classmethod
	async def enable(cls, ticket_id: str, state: FSMContext) -> bool:
		try:
			async with state.proxy() as fsm_data_proxy:
				fsm_data_proxy[ticket_id][cls.Schema.status] = 0
			return True
		except Exception as e:
			logger.error(e)
			logger.error("Can't enable support")
			return False
	
	@staticmethod
	async def freeze(ticket_id: str, state: FSMContext) -> bool:
		try:
			async with state.proxy() as fsm_data_proxy:
				fsm_data_proxy[ticket_id]['state'] = 1
			return True
		except Exception as e:
			logger.error(e)
			logger.error('Can\'t freeze support')
			return False
	
	@staticmethod
	async def delete(*, state: FSMContext, ticket_id: str) -> bool:
		try:
			async with state.proxy() as fsm_data_proxy:
				fsm_data_proxy.pop(ticket_id)
		except Exception as e:
			logger.error(e)
			logger.error("Can't delete support")
			return False
	
	@staticmethod
	async def get_all(state: FSMContext) -> dict:
		try:
			return await state.get_data()
		except Exception as e:
			logger.error(e)
			logger.error('Can\'t get all user\'s tickets')
			return dict()
