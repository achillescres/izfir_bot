from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return isinstance(message.chat.type, types.ChatType.PRIVATE)
