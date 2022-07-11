# from .tickets import dp
# from .clear import dp
from .misc import dp
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
