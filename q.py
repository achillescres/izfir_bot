from pprint import pprint
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from motor.core import AgnosticCollection

import uuid
from pymongo.collection import Collection
from pymongo.database import Database


async def add_faculty(key: str, name: str, collection: AgnosticCollection):
    data = {
        "faculty": {
            'key': key,
            'name': name
        },
        "qus_ans_calls": [],
        "normal_qus_ans": []
    }
    await collection.insert_one(data)

client: AsyncIOMotorClient = AsyncIOMotorClient('localhost', 27017)
db: AsyncIOMotorDatabase = client.izfir
faculties: AsyncIOMotorCollection = db.qus_ans_calls

loop = client.get_io_loop()
# loop.run_until_complete(add_qu_an(faculties, {'qu': 'suksuka', 'an': 'ukasukas'}, 'avt'))
facs = ["АВТОДОРОЖНЫЙ ФАКУЛЬТЕТ", "ГОРНЫЙ ИНСТИТУТ", "ГЕОЛОГОРАЗВЕДОЧНЫЙ ФАКУЛЬТЕТ", "ИНСТИТУТ ЕСТЕСТВЕННЫХ НАУК", "ИНСТИТУТ ЗАРУБЕЖНОЙ ФИЛОЛОГИИ И РЕГИОНОВЕДЕНИЯ", "ИНСТИТУТ МАТЕМАТИКИ И ИНФОРМАТИКИ", "ИНСТИТУТ ПСИХОЛОГИИ", "ИНЖЕНЕРНО-ТЕХНИЧЕСКИЙ ИНСТИТУТ", "ИСТОРИЧЕСКИЙ ФАКУЛЬТЕТ", "ИНСТИТУТ ФИЗИЧЕСКОЙ КУЛЬТУРЫ И СПОРТА", "ИНСТИТУТ ЯЗЫКОВ И КУЛЬТУРЫ НАРОДОВ СЕВЕРО-ВОСТОКА РОССИЙСКОЙ ФЕДЕРАЦИИ", "МЕДИЦИНСКИЙ ИНСТИТУТ", "ПЕДАГОГИЧЕСКИЙ ИНСТИТУТ", "ФИЛОЛОГИЧЕСКИЙ ФАКУЛЬТЕТ", "ФИЗИКО-ТЕХНИЧЕСКИЙ ИНСТИТУТ", "ФИНАНСОВО-ЭКОНОМИЧЕСКИЙ ИНСТИТУТ", "ЮРИДИЧЕСКИЙ ФАКУЛЬТЕТ", "ПОЛИТЕХНИЧЕСКИЙ ИНСТИТУТ (ФИЛИАЛ) СВФУ В Г. МИРНОМ", "ТЕХНИЧЕСКИЙ ИНСТИТУТ (ФИЛИАЛ) СВФУ В Г. НЕРЮНГРИ", "ЧУКОТСКИЙ ФИЛИАЛ СВФУ В Г. АНАДЫРЕ"]

for i in facs:
    loop.run_until_complete(add_faculty(str(uuid.uuid4())[:5], i, faculties))
