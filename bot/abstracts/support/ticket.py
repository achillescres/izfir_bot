from enum import Enum

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from loguru import logger

from bot.abstracts import AbstractMenu
from bot.keyboards.inline import operator_faculties_ikb
from bot.states import MenuFSM
from bot.utils import http
from bot.utils.http.requests import post
from data.config import SERVER_API


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
	# CLOSE TICKET: change state, flush mem, send menu
	async def end_ticket_creation(cls, message: types.Message, state: FSMContext, ticket_id: bool | str = False):
		await AbstractMenu.send(message)
		await state.set_state(MenuFSM.main)
		await cls.flush_ticket_creation_data(state, ticket_id)
	
	@staticmethod
	async def flush_ticket_creation_data(state: FSMContext, ticket_id: bool | str = False):
		async with state.proxy() as fsm_data_proxy:
			if 'faculties_message' in fsm_data_proxy:
				fsm_data_proxy.pop('faculties_message')
			else:
				logger.warning('Can\'t delete faculties_message maybe it already deleted')
			
			if 'faculty_hash' in fsm_data_proxy:
				fsm_data_proxy.pop('faculty_hash')
			else:
				logger.warning('Can\'t delete faculty_hash maybe it already deleted')
			
			if ticket_id and ticket_id in fsm_data_proxy:
				fsm_data_proxy.pop(ticket_id)
	
	@classmethod
	async def create(cls, *, state: FSMContext, user_id: str) -> bool:
		try:
			async with state.proxy() as fsm_data_proxy:
				qu_text: str = fsm_data_proxy.get('qu')
				faculty_hash: str = fsm_data_proxy.get('faculty_hash')
				# Запрос на апи для создания тикета
				res: str = await http.chat.send_ticket(
					client_id=user_id,
					qu_text=qu_text,
					faculty=operator_faculties_ikb.hash_to_name[faculty_hash]
				)
				
				if res in ['err', 'null', '']:
					raise ValueError('Returned ObjectId')
				ticket_id = f"ticket_{res}"
				try:
					fsm_data_proxy[ticket_id] = cls.new(qu_text)
				except Exception as e:
					logger.error(e)
					logger.error("Can't set ticket_id")
					await state.update_data(ticket_id=cls.new(qu_text))
			
			return True
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
	async def delete(*, state: FSMContext, ticket_id: str | None) -> bool:
		if ticket_id is None or ticket_id in ('', 'null'):
			logger.warning('ticket_id is None or empty')
			return True
		try:
			async with state.proxy() as fsm_data_proxy:
				fsm_data_proxy.pop(ticket_id)
				res = await post(f'{SERVER_API}/deleteTicket', data={'user_id': ticket_id})
				
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
	
	# @staticmethod
	# async def set_all(*, dp: Dispatcher, state: FSMContext):
	# 	fsm_data = await AbstractTicket.get_all(state)
	# 	ticket_ids = [
	# 		ticket_id for ticket_id in fsm_data if ticket_id.isnumeric()
	# 	]
