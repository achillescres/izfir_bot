from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

iqu_self_kb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Вернуться к вопросам',
                                 callback_data='return')
        ]]
)
