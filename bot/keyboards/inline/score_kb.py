from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_ikb(ticket_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=str(score), callback_data=f'score_{score}_{ticket_id}')
            for score in range(1, 5 + 1)
        ]]
    )
