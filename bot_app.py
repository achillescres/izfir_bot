import logging

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


async def on_startup(dp: Dispatcher):
    from bot.utils.notify_admin import on_startup_notify
    await on_startup_notify(dp)

    from bot.utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    print('Bot started')


async def on_shutdown(dp: Dispatcher):
    logging.warning('Shutting down!..')

    await dp.bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.info('Bot shut down! Bye!')


class IzfirBot:
    dp = None

    def __init__(self, dev: bool = False):
        self.dev = dev

    def register_trash(self):
        self.dp.register_message_handler(trash, state=MenuFSM.main)

    def _load_questions(self):
        client = MongoClient()
        questions = client.faculties.questions
        data = list(questions.find())
        questions = data
        answers = dict()
        faculties_names = []
        faculties_names_hash = []
        hash_name_to_faculty = {}
        for faculty_obj in questions:
            faculties_names.append(faculty_obj['faculty']['name'])
            faculties_names_hash.append(str(hash(faculties_names[-1])))
            hash_name_to_faculty[faculties_names_hash[-1]] = faculties_names[-1]
            for qu_an_call in faculty_obj['qus_ans_calls']:
                answers[qu_an_call['call']] = qu_an_call['an']

        @self.dp.message_handler(Text(questions_menu_kb.Texts.qus_ans.value), state=MenuFSM.main)
        async def faculties(message: types.Message):
            await message.answer('Выберите факультет', reply_markup=get_faculties_menu_kb(questions))

        print(questions)
        faculties_ikbs = faculties_menu_kb.get_faculty_qus_ans_ikbs(questions)

        @self.dp.message_handler(Text(faculties_ikbs.keys()), state=MenuFSM.main)
        async def faculties_self(message: types.Message):
            await message.answer(message.text, reply_markup=faculties_ikbs[message.text])

        return_to_faculty_ikbs = {
            faculties_names[i]: InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text='Вернуться к вопросам', callback_data=faculty_name_hash)
            )
            for i, faculty_name_hash in enumerate(faculties_names_hash)
        }

        @self.dp.callback_query_handler(text=answers.keys(), state=MenuFSM.main)
        async def question_call(call: types.CallbackQuery):
            await self.dp.bot.answer_callback_query(call.id)
            await call.message.edit_text(answers[call.data], reply_markup=return_to_faculty_ikbs[call.message.text])

        @self.dp.callback_query_handler(text=faculties_names_hash, state=MenuFSM.main)
        async def return_to_faculty_questions(call: types.CallbackQuery):
            await self.dp.bot.answer_callback_query(call.id)
            await call.message.edit_text(hash_name_to_faculty[call.data], reply_markup=faculties_ikbs[hash_name_to_faculty[call.data]])

    def load_questions(self):
        if self.dev:
            self._load_questions()
            return

        try:
            self._load_questions()
        except Exception as e:
            logging.error(f'Error while loading questions from db: {e}')

    async def start(self, WEBHOOK_URL):
        try:
            from bot.handlers import dp
            self.dp = dp
            await on_startup(self.dp)

            self.load_questions()
            # self.register_trash()

            webhook_info = await self.bot.get_webhook_info()
            if webhook_info.url != WEBHOOK_URL:
                await self.bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)

            print('IzfirBot: Dispatcher loaded')
        except Exception as e:
            await self.shutdown()
            logging.error(f"Couldn't start bot \n{e}")
            exit(-1)

    async def shutdown(self):
        try:
            await on_shutdown(self.dp)
            await self.dp.bot.close()
            self.dp = None
        except Exception as e:
            self.dp = None
            logging.error(f"Couldn't correctly shutdown bot\n{e}")

        logging.info('Bot shutted down!')

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
            telegram_update = types.Update(**update)
            Dispatcher.set_current(self.dp)
            Bot.set_current(self.bot)
            await self.dp.process_update(telegram_update)
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
