from io import BytesIO

import aiohttp
import ujson
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from bot.states import ChatFSM
from data.config import SERVER_API
from loader import dp

type_to_bytes = {
	'photo': lambda message: message.photo[-1].download,
	'video': lambda message: message.video.download,
	'document': lambda message: message.document.download
}


@dp.message_handler(
	content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.DOCUMENT],
	state=ChatFSM.chat
)
async def file(message: types.Message, state: FSMContext):
	file_io = BytesIO()
	file_name = ''
	if message.content_type == 'photo':
		file_name = f"{message.photo[-1].file_unique_id}.jpg"
	if message.content_type == 'video':
		file_name = f"{message.video.file_unique_id}.{message.video.file_name.split('.')[-1]}"
	if message.content_type == 'document':
		file_name = f"{message.document.file_unique_id}.{message.document.file_name.split('.')[-1]}"
	# await message.video.download(destination_file=file_io)
	await type_to_bytes[message.content_type](message)(destination_file=file_io)
	async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
		files = {"file": file_io.getvalue()}
		file_io.close()
		operator_id = (await state.get_data()).get('operator_id')
		if not operator_id:
			pass
		
		async with session.post(
				f'{SERVER_API}/fromBot/message/file/?chat_room_id={operator_id}&file_name={file_name}',
				data=files
		) as resp:
			if not resp.ok:
				await message.reply('(Бот) Что-то пошло не так файл не отправлен')
