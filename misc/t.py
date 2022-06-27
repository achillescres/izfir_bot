import asyncio

from aioredis import Redis
from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient


async def main():
	coll: AgnosticCollection = AsyncIOMotorClient("mongodb://localhost:27017").izfir.bot_users
	ticket_id = '123123123'
	print((
		await coll.update_one(
			{'user_id': "1"},
			{'$set': {f'tickets.{ticket_id}': '0'}},
		)).raw_result
	)

if __name__ == '__main__':
	asyncio.run(main())
