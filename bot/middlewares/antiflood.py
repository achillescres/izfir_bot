import asyncio
from loguru import logger

from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from bot.states import MenuFSM
from data.config import DEFAULT_RATE_LIMIT, DEFAULT_SPAM_STUN


def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        if key:
            setattr(func, "throttling_key", key)
        return func
    
    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()
    
    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message

        :param message:
        """
        # Get current handler
        handler = current_handler.get()
        
        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        
        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t)
            
            # Cancel current handler
            raise CancelHandler()
    
    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed

        :param message:
        :param throttled:
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"
        
        # Calculate how many time is left till the block ends
        delta = DEFAULT_SPAM_STUN - throttled.delta
        
        # Check user state
        state = dispatcher.current_state(user=message.from_user.id, chat=message.from_user.id)
        state_state = await state.get_state()
        
        logger.info(f"Middleware: {state_state}")
        if state_state == MenuFSM.stun.state:
            raise CancelHandler()
        
        # Prevent flooding
        if 4 <= throttled.exceeded_count:
            await message.reply(f'(Бот) Не спамьте пожалуйста, подождите {int(round(delta))} секунды')
        
            # Locking state
            await state.set_state(MenuFSM.stun)
            
            # Compute delay
            logger.info(f'Locking user for {delta} seconds')
            
            async def return_main():
                await asyncio.sleep(delta)
                await message.reply('(Бот) Ура, вы можете писать!')
                await state.set_state(MenuFSM.main)
                logger.warning('THIS HAPPENED RETURNED TO MAIN AFTER ANTISPAM')
    
            # Sleep.
            asyncio.create_task(return_main())
            
            raise CancelHandler()

# class ThrottlingMiddleware(BaseMiddleware):
#
#     def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
#         self.rate_limit = limit
#         self.prefix = key_prefix
#         super(ThrottlingMiddleware, self).__init__()
#
#     async def throttle(self, target: types.Message | types.CallbackQuery):
#         handler = current_handler.get()
#         dispatcher = Dispatcher.get_current()
#         if not handler:
#             return
#         limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
#         key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
#
#         try:
#             await dispatcher.throttle(key, rate=limit)
#         except Throttled as t:
#             await self.target_throttled(target, t, dispatcher, key)
#             raise CancelHandler()
#
#     @staticmethod
#     async def target_throttled(target: types.Message | types.CallbackQuery,
#                                throttled: Throttled, dispatcher: Dispatcher, key: str):
#         msg = target.message if isinstance(target, types.CallbackQuery) else target
#         delta = throttled.rate - throttled.delta
#         print(delta)
#
#         if throttled.exceeded_count >= 3:
#             await msg.reply(f'(Бот) Не спамьте. Подождите {int(round(delta))} секунд')
#             raise CancelHandler()
#
#         await asyncio.sleep(delta)
#
#         thr = await dispatcher.check_key(key)
#         if thr.exceeded_count == throttled.exceeded_count:
#             await msg.reply("(Бот) Можете писать")
#
#     async def on_process_message(self, message, data):
#         await self.throttle(message)
#
#     async def on_process_callback_query(self, call, data):
#         await self.throttle(call)


# class ThrottlingMiddleware(BaseMiddleware):
#     def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
#         self.rate_limit = limit
#         self.prefix = key_prefix
#         super(ThrottlingMiddleware, self).__init__()
#
#     async def on_process_message(self, message: types.Message, data: dict):
#         """
#         This handler is called when dispatcher receives a message
#
#         :param message:
#         """
#         # Get current handler
#         handler = current_handler.get()
#
#         # Get dispatcher from context
#         dispatcher = Dispatcher.get_current()
#         # If handler was configured, get rate limit and key from handler
#         if handler:
#             limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
#             key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
#         else:
#             limit = self.rate_limit
#             key = f"{self.prefix}_message"
#
#         # Use Dispatcher.throttle method.
#         try:
#             await dispatcher.throttle(key, rate=limit)
#         except Throttled as t:
#             # Execute action
#             await self.message_throttled(message, t)
#
#             # Cancel current handler
#             raise CancelHandler()
#
#     async def message_throttled(self, message: types.Message, throttled: Throttled):
#         """
#         Notify user only on first exceed and notify about unlocking only on last exceed
#
#         :param message:
#         :param throttled:
#         """
#         handler = current_handler.get()
#         dispatcher = Dispatcher.get_current()
#         if handler:
#             key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
#         else:
#             key = f"{self.prefix}_message"
#
#         # Calculate how many time is left till the block ends
#         delta = DEFAULT_SPAM_STUN - throttled.delta
#
#         # Check user state
#         state = dispatcher.current_state(user=message.from_user.id, chat=message.from_user.id)
#         state_state = await state.get_state()
#         if state_state == MenuFSM.stun.state:
#             raise CancelHandler()
#
#         # Prevent flooding
#         if throttled.exceeded_count <= 3:
#             await message.reply('(Бот) Не спамьте пожалуйста, подождите 2 секунды')
#
#         # Sleep.
#         await state.set_state(MenuFSM.stun)
#         await asyncio.sleep(delta)
#         await state.set_state(MenuFSM.main)
#
#         # Check lock status
#         thr = await dispatcher.check_key(key)
#
#         # If current message is not last with current key - do not send message
#         if thr.exceeded_count == throttled.exceeded_count:
#             await message.reply('(Бот) Ура, вы можете писать!')
#         else:
#             raise CancelHandler()
