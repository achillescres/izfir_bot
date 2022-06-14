import logging

import motor.motor_asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.webhook import AnswerCallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

from bot.keyboards.default.menu import menu_kb
from bot.keyboards.default.questions import questions_menu_kb
from bot.keyboards.default.questions.qus_ans import faculties_menu_kb
from bot.keyboards.default.questions.qus_ans.faculties_menu_kb import get_faculties_menu_kb
from bot.states import MenuFSM
from bot.static_handlers import trash


class Questions(object):
    async def init(self):
        self.questions = None
        self.return_to_faculty_ikbs = None
        self.faculties_ikbs = None
        self.answers = dict()
        self.faculties_names = []
        self.faculties_names_hash = []
        self.hash_name_to_faculty = {}
        self.db = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb://localhost:27017"
        ).izfir
        self.qus_ans_calls_collection = self.db.qus_ans_calls

        await self.update_data()

    async def _load_from_db(self):
        self.questions = await self.qus_ans_calls_collection.find().to_list(40)
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


class IzfirBot:
    dp = None

    def __init__(self, dev: bool = False):
        self.dev = dev
        self.data_proxy = Questions()

    def register_trash(self):
        self.dp.register_message_handler(trash, state=MenuFSM.main)

    async def _set_questions_handlers(self):
        @self.dp.message_handler(Text(questions_menu_kb.Texts.qus_ans.value), state=MenuFSM.main)
        async def faculties(message: types.Message):
            proxy = self.data_proxy
            await message.answer('Выберите факультет', reply_markup=get_faculties_menu_kb(proxy.questions))

        @self.dp.message_handler(Text(self.data_proxy.faculties_ikbs.keys()), state=MenuFSM.main)
        async def faculties_self(message: types.Message):
            await message.answer(message.text, reply_markup=self.data_proxy.faculties_ikbs[message.text])

        @self.dp.callback_query_handler(text=self.data_proxy.answers.keys(), state=MenuFSM.main)
        async def question_call(call: types.CallbackQuery):
            await self.dp.bot.answer_callback_query(call.id)
            await call.message.edit_text(self.data_proxy.answers[call.data], reply_markup=self.data_proxy.return_to_faculty_ikbs[call.message.text])

        @self.dp.callback_query_handler(text=self.data_proxy.faculties_names_hash, state=MenuFSM.main)
        async def return_to_faculty_questions(call: types.CallbackQuery):
            await self.dp.bot.answer_callback_query(call.id)
            await call.message.edit_text(self.data_proxy.hash_name_to_faculty[call.data], reply_markup=self.data_proxy.faculties_ikbs[self.data_proxy.hash_name_to_faculty[call.data]])

    async def update_questions(self):
        await self.data_proxy.update_data()

    async def start(self, WEBHOOK_URL):
        try:
            from bot.handlers import dp
            self.dp = dp
            await self.data_proxy.init()
            await self.on_startup()
            await self._set_questions_handlers()
            # self.register_trash()

            webhook_info = await self.bot.get_webhook_info()
            if webhook_info.url != WEBHOOK_URL:
                await self.bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)

            print('IzfirBot: Dispatcher loaded')
        except Exception as e:
            await self.shutdown()
            logging.error(f"Couldn't start bot \n{e}")
            exit(-1)

    async def on_startup(self):
        from bot.utils.notify_admin import on_startup_notify
        await on_startup_notify(self.dp)

        from bot.utils.set_bot_commands import set_default_commands
        await set_default_commands(self.dp)

    async def shutdown(self):
        try:
            logging.warning('Shutting down!..')

            await self.dp.bot.delete_webhook()
            await self.dp.storage.close()
            await self.dp.storage.wait_closed()

            del self.dp
            logging.info('Shutdown correct')
        except Exception as e:
            del self.dp
            logging.error(f"Couldn't correctly shutdown bot\n{e}")

    async def _update(self, update: dict):
        telegram_update = types.Update(**update)
        Dispatcher.set_current(self.dp)
        Bot.set_current(self.bot)
        await self.dp.process_update(telegram_update)

    async def update(self, update: dict):
        if self.dev:
            await self._update(update)
            return

        try:
            await self._update(update)
        except Exception as e:
            logging.error(f'Update error {e}')

    async def send_message(self, text, user_id, kb=menu_kb.kb):
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=f"(Оператор): {text}",
                reply_markup=kb
            )
        except Exception as e:
            logging.error(f"send_message error {e}")

    @property
    def bot(self):
        return self.dp.bot
