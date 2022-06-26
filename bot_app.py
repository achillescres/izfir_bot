import logging

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import Text

from bot.abstracts.questions_proxy_storage import QuestionsProxyStorage
from bot.keyboards.default.chat import chat_kbs
from bot.keyboards.default.menu import menu_kb
from bot.keyboards.default.questions.qus_ans.faculties_menu_kb import get_faculties_menu_kb
from bot.states import MenuFSM
from bot.static_handlers import after_start_trash, before_start_trash


class TelegramBot:
    dp = None

    def __init__(self, dev: bool = False):
        self.dev = dev
        self.data_proxy = QuestionsProxyStorage()

    def _register_trash_handlers(self):
        self.dp.register_message_handler(after_start_trash.handler, **after_start_trash.options)
        self.dp.register_message_handler(before_start_trash.handler, **before_start_trash.options)

    async def _set_static_handlers(self):
        # For dynamic data closure
        @self.dp.message_handler(Text(menu_kb.Texts.qus.value), state=MenuFSM.main)
        async def faculties(message: types.Message):
            await message.answer('Выберите факультет', reply_markup=get_faculties_menu_kb(self.data_proxy.questions))

        @self.dp.message_handler(Text(self.data_proxy.faculties_ikbs.keys()), state=MenuFSM.main)
        async def faculties_self(message: types.Message):
            await message.answer(message.text, reply_markup=self.data_proxy.faculties_ikbs[message.text])

        @self.dp.callback_query_handler(text=self.data_proxy.answers.keys(), state=MenuFSM.main)
        async def question_call(call: types.CallbackQuery):
            await self.dp.bot.answer_callback_query(call.id)
            await call.message.edit_text(self.data_proxy.answers[call.data],
                                         reply_markup=self.data_proxy.return_to_faculty_ikbs[call.message.text])

        @self.dp.callback_query_handler(text=self.data_proxy.faculties_names_hash, state=MenuFSM.main)
        async def return_to_faculty_questions(call: types.CallbackQuery):
            await self.dp.bot.answer_callback_query(call.id)
            await call.message.edit_text(
                self.data_proxy.hash_name_to_faculty[call.data],
                reply_markup=self.data_proxy.faculties_ikbs[self.data_proxy.hash_name_to_faculty[call.data]]
            )

        # trash handler must be in the end
        self._register_trash_handlers()

    async def update_questions(self):
        await self.data_proxy.update_data()

    async def start(self, WEBHOOK_URL):
        try:
            from bot.handlers import dp
            self.dp = dp
            await self.data_proxy.init()
            await self.on_startup()
            await self._set_static_handlers()

            webhook_info = await self.bot.get_webhook_info()
            if webhook_info.url != WEBHOOK_URL:
                await self.bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)

            logging.info('IzfirBot: Dispatcher loaded')
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
            logging.error(f"Couldn't correctly shutdown bot\n{e}")
            self.dp = None
        finally:
            logging.warning('Bye!')

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

    async def send_message(self, text, user_id, operator_name='Оператор', reply_markup=chat_kbs.finish_chat_kb):
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=f"{operator_name}: {text}",
                reply_markup=reply_markup
            )
        except Exception as e:
            logging.error(f"send_message error {e}")

    @property
    def bot(self):
        return self.dp.bot
