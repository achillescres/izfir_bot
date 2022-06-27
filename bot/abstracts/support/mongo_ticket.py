from typing import Optional

from loguru import logger

from motor.core import AgnosticCollection


class Schema:
	state: dict[int, str] = {
		0: 'Ожидание оператора',
		1: 'Ождиание пользователя',
		2: 'Общение'
	}

	question: str
	answer: str | Optional


class Ticket:
	@staticmethod
	async def create(cls, *, user_id: str, ticket_id: str, collection: AgnosticCollection) -> bool:
		return await cls.enable(
			user_id=user_id,
			ticket_id=ticket_id,
			collection=collection
		)
	
	@staticmethod
	async def enable(*, user_id: str, ticket_id: str, collection: AgnosticCollection) -> bool:
		try:
			return bool(
				await collection.update_one(
					{'user_id': user_id},
					{
						'$set': {
							f'tickets.{ticket_id}': 0,
						}
					}
				).raw_result['ok'])
		except Exception as e:
			logger.error(e)
			logger.error("Can't enable support")
			return False
	
	@staticmethod
	async def freeze(*, user_id: str, ticket_id: str, collection: AgnosticCollection) -> bool:
		try:
			return await collection.update_one(
				{'user_id': user_id},
				{
					'$set': {
						f'tickets.{ticket_id}': 1,
					}
				}
			).acknowledged
		except Exception as e:
			logger.error(e)
			logger.error('Can\'t freeze support')
			return False
	
	@staticmethod
	async def delete(*, user_id: str, ticket_id: str, collection: AgnosticCollection) -> bool:
		try:
			return await collection.update_one(
				{'user_id': user_id},
				{
					'$unset': {
						f'tickets.{ticket_id}': 1,
					}
				}
			).acknowledged
		except Exception as e:
			logger.error(e)
			logger.error("Can't delete support")
			return False
	
	@staticmethod
	async def get_user_tickets(user_id: str, collection: AgnosticCollection) -> list:
		try:
			res = await collection.find_one(
				{'user_id': str(user_id)},
				{'tickets': 1, '_id': 0}
			)
			if not res:
				return []
			
			return res
		except Exception as e:
			logger.error(e)
			logger.error('Cant parse all user\'s tickets')
			return []
