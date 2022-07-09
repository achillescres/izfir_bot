from aiogram import types, Bot

from bot.keyboards.inline import score_kb


async def score_chat_with_bot(user_id: str, ticket_id: str, bot: Bot):
    await bot.send_message(
        text='Сеанс был завершен\nПожалуйста, оцените качество техподдержки',
        chat_id=user_id,
        reply_markup=score_kb.get_ikb(ticket_id=ticket_id)
    )
    

async def score_chat_with_message(ticket_id: str, message: types.Message):
    await message.answer(
        text="Сеанс был завершен\nПожалуйста, оцените качество техподдержки",
        reply_markup=score_kb.get_ikb(ticket_id=ticket_id)
    )
