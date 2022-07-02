import aiohttp
import ujson
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.abstracts.support import AbstractTicket
from bot.keyboards.default.menu import menu_kb
from bot.states import ChatFSM, MenuFSM
from data.config import SERVER_API
from loader import dp


@dp.message_handler(text=['1', '2', '3', '4', '5'], state=ChatFSM.estimate)
async def estimate_ticket(message: types.Message, state: FSMContext):
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:

        operator_id = (await state.get_data()).get('operator_id')
        if not operator_id:
            pass
        data = {
            'chat_room_id': operator_id,
            'star': message.text
        }

        async with session.post(
                f'{SERVER_API}/fromBot/message/estimate', json=data
        ) as resp:
            if not resp.ok:
                await message.reply('(Бот) Что-то пошло не так файл не отправлен')
        await session.close()
    await state.set_state(MenuFSM.main)
    await AbstractTicket.delete(
        ticket_id=(await state.get_data()).get('ticket_id'),
        state=state
    )
    await message.answer("Главное меню", reply_markup=menu_kb.kb)
