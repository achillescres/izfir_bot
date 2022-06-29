from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.abstracts import TextEnum


class Texts(TextEnum):
	return_to_menu_data = 'mainmenu'


def _ikb(tickets: Iterable[tuple[str, str]]):
	return InlineKeyboardMarkup(
		row_width=1,
		inline_keyboard=[
			[InlineKeyboardButton(text=qu_text, data=data)] for qu_text, data in tickets
		]
	)


def ikb(tickets: tuple[tuple[int, str]]):
	return InlineKeyboardMarkup(
		row_width=5,
		inline_keyboard=[
			[InlineKeyboardButton(text=str(index - 1), callback_data=ticket_id) for index, ticket_id in tickets[i:i + 5]] for i in range(0, len(tickets), 5)
		]
	)
