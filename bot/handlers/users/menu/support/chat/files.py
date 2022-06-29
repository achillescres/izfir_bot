# in-in-dev
from aiogram import types
from aiogram.types import ContentType
from loguru import logger

from bot.states import ChatFSM, MenuFSM
from loader import dp


@dp.message_handler(
	content_types=[ContentType.PHOTO],
	state=MenuFSM.main
)
async def photo(message: types.Message):
	logger.info(message.photo)
	for i in message.photo:
		await message.answer(i.file_id)


@dp.message_handler(
	content_types=[ContentType.VIDEO],
	state=MenuFSM.main
)
async def video(message: types.Message):
	await message.answer(message.video.file_id)


@dp.message_handler(
	content_types=[ContentType.DOCUMENT],
	state=MenuFSM.main
)
async def document(message: types.Message):
	await message.answer(message.document.file_id)
