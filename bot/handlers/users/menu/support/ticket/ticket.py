import aiohttp
import ujson
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger

from bot.abstracts.support import AbstractTicket
from bot.keyboards.default.menu import menu_kb
from bot.keyboards.inline import operator_faculties_ikb
from bot.keyboards.inline.operator_faculties_ikb import hashes
from bot.states.machines import ChatFSM
from data.config import SERVER_API
from loader import dp

from bot.keyboards.default.chat import chat_kbs

from bot.states import MenuFSM


# HERE WE CREATING TICKET ->

# > FACULTY LIST == ChatFSM.choosing_faculty

# --> OPEN FACULTY LIST
@dp.message_handler(text=menu_kb.Texts.chat.value, state=MenuFSM.main)
async def faculties(message: types.Message, state: FSMContext):
    await (await message.answer('Обработка...', reply_markup=types.ReplyKeyboardRemove())).delete()
    mes = await message.answer('Выберите тип оператора', reply_markup=operator_faculties_ikb.ikb)
    await state.update_data(faculties_message=mes.to_python())
    await state.set_state(ChatFSM.choosing_faculty)


# CLOSE FACULTY LIST --> MAIN MENU
@dp.callback_query_handler(text=hashes[0], state=ChatFSM.choosing_faculty)
async def return_to_menu_with_call(call: types.CallbackQuery, state: FSMContext):
    await dp.bot.answer_callback_query(call.id)
    
    async with state.proxy() as fsm_data_proxy:
        faculties_message_json = fsm_data_proxy.get('faculties_message')
        if faculties_message_json is not None:
            await types.Message.to_object(
                data=faculties_message_json
            ).delete()

    await AbstractTicket.end_ticket_creation(call.message, state)


# CLICK ON IKB FACULTY LIST --> QU INPUT
@dp.callback_query_handler(text=operator_faculties_ikb.hash_to_name, state=ChatFSM.choosing_faculty)
async def get_qu(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as fsm_data_proxy:
        faculties_message: dict = fsm_data_proxy.get('faculties_message')
        if faculties_message is None:
            await AbstractTicket.end_ticket_creation(call.message, state)
            return

        await (types.Message.to_object(data=faculties_message)).edit_text(
            text=operator_faculties_ikb.hash_to_name[call.data],
            reply_markup=None
        )
        
        await call.message.answer(
            'Сформулируйте и напишите свой вопрос',
            reply_markup=chat_kbs.close_qu_kb
        )
        
        await dp.bot.answer_callback_query(call.id)
        
        await state.set_state(ChatFSM.writing_qu)
        fsm_data_proxy['faculty_hash'] = call.data
        fsm_data_proxy.pop('faculties_message')


# --> QU INPUT == ChatFSM.writing_qu

# CLOSE QU INPUT --> MAIN MENU
@dp.message_handler(text=chat_kbs.Texts.close_qu.value, state=ChatFSM.writing_qu)
async def return_to_menu_message(message: types.Message, state: FSMContext):
    await AbstractTicket.end_ticket_creation(message, state)


# GET QU INPUT --> QU APPLY
@dp.message_handler(state=ChatFSM.writing_qu)
async def set_qu(message: types.Message, state: FSMContext):
    await message.reply('Вы уверены в правильности вопроса?', reply_markup=chat_kbs.apply_chat_kb)
    await state.set_state(ChatFSM.apply_qu)
    await state.update_data(qu=message.text)


# --> QU APPLY == ChatFSM.apply_qu

# CLOSE QU APPLY --> MAIN MENU == None !
@dp.message_handler(text=chat_kbs.Texts.close_qu.value, state=ChatFSM.apply_qu)
async def close_qu(message: types.Message, state: FSMContext):
    await AbstractTicket.end_ticket_creation(message, state)


# EDIT QU APPLY --> QU INPUT <-> UP == ChatFSM.writing_qu
@dp.message_handler(text=chat_kbs.Texts.discard_qu.value, state=ChatFSM.apply_qu)
async def edit_qu(message: types.Message, state: FSMContext):
    await message.answer('Сформулируйте и напишите свой вопрос', reply_markup=chat_kbs.close_qu_kb)
    await state.set_state(ChatFSM.writing_qu)


@dp.message_handler(state=ChatFSM.waiting_chat)
async def waiting_chat_trash(message: types.Message):
    await message.reply('Подождите конца обработки заявки')


# APPLY QU APPLY --> None
@dp.message_handler(text=chat_kbs.Texts.apply_qu.value, state=ChatFSM.apply_qu)
async def create_ticket(message: types.Message, state: FSMContext):
    waiting_message: types.Message = await message.answer('Обработка...', reply_markup=None)
    await state.set_state(ChatFSM.waiting_chat)

    res: bool = await AbstractTicket.create(
        state=state,
        user_id=message.from_user.id
    )

    if not res:
        await waiting_message.edit_text('Извините! Что-то пошло не так.\nПопробуйте ещё раз через минуту')
        return

    await waiting_message.edit_text(
        'Ваша заявка отправлена, вам напишет первый освободившийся оператор, будьте терпеливы',
    )

    await AbstractTicket.end_ticket_creation(message, state)


# HERE WE HANDLING TICKET SCORE
@dp.callback_query_handler(Text(startswith='score_'), state='*')
async def score_ticket(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    _, score, ticket_id = data.split('_')

    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        data = {
            'chat_room_id': ticket_id,
            'star': score
        }
    
        async with session.post(
                f'{SERVER_API}/fromBot/message/estimate', json=data
        ) as resp:
            if not resp.ok:
                await call.message.edit_text(f'Вы поставили оценку {score}')
            else:
                logger.error(f"Can't send ticket score to server\nResponse: {await resp.read()}")
        await session.close()
