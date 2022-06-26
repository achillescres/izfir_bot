import logging

from aioredis import Redis


class AbstractTicket:
	@classmethod
	async def create(cls, *, user_id: str, ticket_id: str, redis: Redis):
		return await cls.enable(
			user_id=user_id,
			ticket_id=ticket_id,
			redis=redis
		)
	
	@staticmethod
	async def enable(*, user_id: str, ticket_id: str, redis: Redis) -> bool:
		try:
			await redis.set(f'{user_id}:{ticket_id}:', True)
			return True
		except Exception as e:
			logging.error(e)
			logging.error("Can't enable ticket")
			return False
	
	@staticmethod
	async def freeze(*, user_id: str, ticket_id: str, redis: Redis) -> bool:
		try:
			await redis.set(f'{user_id}:{ticket_id}:', False)
			return True
		except Exception as e:
			logging.error(e)
			logging.error("Can't freeze ticket")
			return False
	
	@staticmethod
	async def delete(*, user_id: str, ticket_id: str, redis: Redis) -> bool:
		try:
			await redis.delete(f'{user_id}:{ticket_id}')
			return True
		except Exception as e:
			logging.error(e)
			logging.error("Can't delete ticket")
			return False
