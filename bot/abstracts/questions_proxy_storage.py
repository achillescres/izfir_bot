import motor.motor_asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.default.questions.qus_ans import faculties_menu_kb


class QuestionsProxyStorage(object):
    def __init__(self):
        self.collection = None
        self.db = None

    async def init(self):
        self.db = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb://localhost:27017"
        ).izfir
        self.collection = self.db.qus_ans_calls

        await self.update_data()

    async def _load_from_db(self):
        self.questions = await self.collection.find().to_list(40)
        self.return_to_faculty_ikbs = None
        self.faculties_ikbs = None
        self.answers = dict()
        self.faculties_names = []
        self.faculties_names_hash = []
        self.hash_name_to_faculty = {}

        for faculty_obj in self.questions:
            self.faculties_names.append(faculty_obj['faculty']['name'])
            self.faculties_names_hash.append(str(hash(self.faculties_names[-1])))
            self.hash_name_to_faculty[self.faculties_names_hash[-1]] = self.faculties_names[-1]
            for qu_an_call in faculty_obj['qus_ans_calls']:
                self.answers[qu_an_call['call']] = qu_an_call['an']

        self.faculties_ikbs = faculties_menu_kb.get_faculty_qus_ans_ikbs(self.questions)

        self.return_to_faculty_ikbs = {
            self.faculties_names[i]: InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text='Вернуться к вопросам', callback_data=faculty_name_hash)
            )
            for i, faculty_name_hash in enumerate(self.faculties_names_hash)
        }

    async def update_data(self):
        await self._load_from_db()