import aiohttp
import ujson
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.abstracts.support import AbstractTicket
from bot.keyboards.default.chat import estimate_kb
from bot.keyboards.default.menu import menu_kb
from bot.states import ChatFSM, MenuFSM
from data.config import SERVER_API
from loader import dp


@dp.message_handler(text=estimate_kb.Texts.values(), state=ChatFSM.estimate)
async def estimate_ticket(message: types.Message, state: FSMContext):
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async with state.proxy() as fsm_data_proxy:
            if 'operator_id' in fsm_data_proxy:
                operator_id = fsm_data_proxy.pop('operator_id')
        if operator_id:
            data = {
                'chat_room_id': operator_id,
                'star': message.text
            }

            async with session.post(
                    f'{SERVER_API}/fromBot/message/estimate', json=data
            ) as resp:
                if not resp.ok:
                    await message.reply('Что-то пошло не так! Оценка не отправлена.')
        else:
            await message.reply('Что-то пошло не так! Оценка не отправлена.')
        await session.close()
    await state.set_state(MenuFSM.main)
    await message.answer("Главное меню", reply_markup=menu_kb.kb)

