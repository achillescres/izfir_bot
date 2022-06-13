from pprint import pprint
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from motor.core import AgnosticCollection
from pymongo.collection import Collection
from pymongo.database import Database


async def add_qu_an(collection: AgnosticCollection, qu_an, to_fac_key: str):
    new_not_an_index = (await collection.find_one(
            {'faculty.key': to_fac_key},
            {'qus_ans_calls': {'$slice': -1}}
        ))['qus_ans_calls'][0]['not_an_index'] + 1

    new_call = f'{to_fac_key}_{new_not_an_index}'
    new_qu_an_call = {
        'not_an_index': new_not_an_index,
        'qu': qu_an['qu'],
        'an': qu_an['an'],
        'call': new_call
    }

    await collection.update_one(
        {
            'faculty.key': to_fac_key
        },
        {
            '$push':
                {
                    'qus_ans_calls': new_qu_an_call
                }
        }
    )


client: AsyncIOMotorClient = AsyncIOMotorClient('localhost', 27017)
db: AsyncIOMotorDatabase = client.faculties
faculties: AsyncIOMotorCollection = db.qus_ans_calls

loop = client.get_io_loop()
loop.run_until_complete(add_qu_an(faculties, {'qu': 'suksuka', 'an': 'ukasukas'}, 'avt'))
