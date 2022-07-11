import motor.motor_asyncio
from motor.core import AgnosticCollection

# facs = ["АВТОДОРОЖНЫЙ ФАКУЛЬТЕТ", "ГОРНЫЙ ИНСТИТУТ", "ГЕОЛОГОРАЗВЕДОЧНЫЙ ФАКУЛЬТЕТ", "ИНСТИТУТ ЕСТЕСТВЕННЫХ НАУК",
#         "ИНСТИТУТ ЗАРУБЕЖНОЙ ФИЛОЛОГИИ И РЕГИОНОВЕДЕНИЯ", "ИНСТИТУТ МАТЕМАТИКИ И ИНФОРМАТИКИ", "ИНСТИТУТ ПСИХОЛОГИИ",
#         "ИНЖЕНЕРНО-ТЕХНИЧЕСКИЙ ИНСТИТУТ", "ИСТОРИЧЕСКИЙ ФАКУЛЬТЕТ", "ИНСТИТУТ ФИЗИЧЕСКОЙ КУЛЬТУРЫ И СПОРТА",
#         "ИНСТИТУТ ЯЗЫКОВ И КУЛЬТУРЫ НАРОДОВ СЕВЕРО-ВОСТОКА РОССИЙСКОЙ ФЕДЕРАЦИИ", "МЕДИЦИНСКИЙ ИНСТИТУТ",
#         "ПЕДАГОГИЧЕСКИЙ ИНСТИТУТ", "ФИЛОЛОГИЧЕСКИЙ ФАКУЛЬТЕТ", "ФИЗИКО-ТЕХНИЧЕСКИЙ ИНСТИТУТ",
#         "ФИНАНСОВО-ЭКОНОМИЧЕСКИЙ ИНСТИТУТ", "ЮРИДИЧЕСКИЙ ФАКУЛЬТЕТ",
#         "ПОЛИТЕХНИЧЕСКИЙ ИНСТИТУТ (ФИЛИАЛ) СВФУ В Г МИРНОМ", "ТЕХНИЧЕСКИЙ ИНСТИТУТ (ФИЛИАЛ) СВФУ В Г. НЕРЮНГРИ",
#         "ЧУКОТСКИЙ ФИЛИАЛ СВФУ В Г. АНАДЫРЕ"]


async def get_faculties_names(db: motor.motor_asyncio.AsyncIOMotorClient | None) -> list:
    if db:
        collection: AgnosticCollection = db.qus_ans_calls
    else:
        collection: AgnosticCollection = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017').izfir.qus_ans_calls

    return await collection.find({}, {'faculty.name': 1}).to_list(100)


async def get_hashed_faculties(db: motor.motor_asyncio.AsyncIOMotorClient) -> dict[str, dict]:
    hash_to_name = {
        str(hash(name)): name
        for name in ['Главное меню'] + [faculty_name for faculty_name in await get_faculties_names(db)]
    }
    
    return hash_to_name
