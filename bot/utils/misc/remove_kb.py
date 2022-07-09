from aiogram import types, Bot
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup


async def remove_kb(
		message: types.Message | None = None,
		bot: Bot | None = None,
		user_id: str | None = None,
		text: str = 'Обработка...',
		kb: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None) -> bool:
	try:
		match message:
			case None:
				await bot.send_message(
					chat_id=user_id,
					text=text,
					reply_markup=kb
				)
				return True
			case _:
				await (await message.answer(text, reply_markup=kb)).delete()
				return True
	except:
		return False

		