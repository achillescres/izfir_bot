import motor.motor_asyncio
from loguru import logger

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import Text

from bot.abstracts.questions_proxy_storage import QuestionsProxyStorage
from bot.keyboards.default.chat import chat_kbs
from bot.keyboards.default.menu import menu_kb
from bot.keyboards.default.questions.qus_ans.faculties_menu_kb import get_faculties_menu_kb
from bot.states import MenuFSM
from bot.handlers.static import before_start_trash, all_trash_handler
from bot.handlers.static import after_start_trash


class TelegramBot:
    dp = None
    redis = None
    
    def __init__(self, dev: bool = False):
        self.dev = dev
        self.data_proxy = QuestionsProxyStorage()

    def _register_trash_handlers(self):
        self.dp.register_message_handler(after_start_trash.handler, **after_start_trash.options)
        self.dp.register_message_handler(before_start_trash.handler, **before_start_trash.options)
        self.dp.register_message_handler(all_trash_handler.handler, **all_trash_handler.options)
    
    # For dynamic data closure
    def _set_static_message_handlers(self):
        @self.dp.message_handler(Text(menu_kb.Texts.qus.value), state=MenuFSM.main)
        async def faculties(message: types.Message):
            await message.answer('Выберите факультет', reply_markup=get_faculties_menu_kb(self.data_proxy.questions))

        @self.dp.message_handler(Text(self.data_proxy.faculties_ikbs.keys()), state=MenuFSM.main)
        async def faculties_self(message: types.Message):
            await message.answer(message.text, reply_markup=self.data_proxy.faculties_ikbs[message.text])

    def _set_static_callback_handlers(self):
        @self.dp.callback_query_handler(text=self.data_proxy.answers.keys(), state=MenuFSM.main)
        async def question_call(call: types.CallbackQuery):
            await self.dp.bot.answer_callback_query(call.id)
            answer = self.data_proxy.answers[call.data]
            if not answer:
                answer = 'На данный вопрос пока отсутствует ответ'
            
            await call.message.edit_text(answer,
                                         reply_markup=self.data_proxy.return_to_faculty_ikbs[call.message.text])

        @self.dp.callback_query_handler(text=self.data_proxy.faculties_names_hash, state=MenuFSM.main)
        async def return_to_faculty_questions(call: types.CallbackQuery):
            await self.dp.bot.answer_callback_query(call.id)
            await call.message.edit_text(
                self.data_proxy.hash_name_to_faculty[call.data],
                reply_markup=self.data_proxy.faculties_ikbs[self.data_proxy.hash_name_to_faculty[call.data]]
            )
    
    async def on_startup(self):
        from bot.utils.notify_admin import on_startup_notify
        await on_startup_notify(self.dp)

        from bot.utils.set_bot_commands import set_default_commands
        await set_default_commands(self.dp)
    
    async def start(self, webhook_url: str):
        try:
            from bot.handlers import dp
            self.dp = dp
            db = motor.motor_asyncio.AsyncIOMotorClient(
                "mongodb://localhost:27017"
            ).izfir
            
            # WARNING! ADDING ATTRIBUTE TO OBJECT PROVIDED BY AIOGRAM
            # self.dp.my_mongo_users = db.bot_users
            
            await self.data_proxy.init(db.qus_ans_calls)
            await self.on_startup()
            self._set_static_message_handlers()
            self._set_static_callback_handlers()
            self._register_trash_handlers()

            webhook_info = await self.bot.get_webhook_info()
            if webhook_info.url != webhook_url:
                await self.bot.set_webhook(url=webhook_url, drop_pending_updates=True)
            
            logger.info('IzfirBot: Dispatcher loaded')
        except Exception as e:
            await self.shutdown()
            logger.error(f"Couldn't start bot \n{e}")
            exit(-1)

    async def shutdown(self):
        try:
            logger.warning('Shutting down!..')

            await self.dp.bot.delete_webhook()
            await self.dp.storage.close()
            await self.dp.storage.wait_closed()
            
            del self.dp
            logger.info('Shutdown correct')
            await self.redis.close()
        except Exception as e:
            logger.error(f"Couldn't correctly shutdown bot\n{e}")
            self.dp = None
        finally:
            logger.warning('Bye!')

    async def _telegram_update(self, update: dict):
        telegram_update = types.Update(**update)
        Dispatcher.set_current(self.dp)
        Bot.set_current(self.bot)
        await self.dp.process_update(telegram_update)

    async def telegram_update(self, update: dict):
        if self.dev:
            try:
                user_id = update['message']['chat']['id']
                state = self.dp.current_state(chat=user_id, user=user_id)
                logger.info(
                    f"Providing update for user {user_id}\nUser's current state: {(await state.get_state())}"
                )
            except KeyError:
                logger.warning("Update not for user")
            
            await self._telegram_update(update)
            return
        try:
            await self._telegram_update(update)
        except Exception as e:
            logger.error(e)
            logger.error("Can't provide telegram update")

    async def send_message(self, text, user_id, operator_name='Оператор', reply_markup=chat_kbs.finish_chat_kb):
        try:
            # _operator_name = (await self.dp.current_state(chat=user_id, user=user_id).get_data()).get('operator_name')
            # if operator_name:
            #     operator_name = _operator_name
            await self.bot.send_message(
                chat_id=user_id,
                text=f"{operator_name}: {text}",
                reply_markup=reply_markup
            )
        except Exception as e:
            logger.error(f"send_message error {e}")
    
    async def update_question(self):
        await self.data_proxy.update_data()
        self._set_static_callback_handlers()
    
    @property
    def bot(self):
        return self.dp.bot
