from io import BytesIO

import aiohttp
import ujson
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from bot.states import ChatFSM, MenuFSM
from data.config import SERVER_API
from loader import dp

type_to_bytes = {
	'photo': lambda message: message.photo[-1].download,
	'video': lambda message: message.video.download,
	'document': lambda message: message.document.download
}


@dp.message_handler(
	content_types=[ContentType.PHOTO, ContentType.VIDEO, ContentType.DOCUMENT],
	state=MenuFSM.main
)
async def file(message: types.Message, state: FSMContext):
	await state.update_data(operator_id='123')
	file_io = BytesIO()
	
	await message.video.download(destination_file=file_io)
	# await type_to_bytes[message.content_type](message)(destination_file=file_io)
	async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
		files = {'file': file_io.getvalue()}
		file_io.close()
		chat_room_id = (await state.get_data()).get('operator_id')
		if not chat_room_id:
			pass
		
		async with session.post(f'{SERVER_API}/fromBot/message/file/?chat_room_id={chat_room_id}', data=files) as resp:
			if not resp.ok:
				await message.reply('(Бот) Что-то пошло не так файл не отправлен')
		await session.close()
	
	await state.update_data(operator_id=None)
