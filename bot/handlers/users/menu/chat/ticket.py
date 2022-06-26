from uuid import uuid4

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.abstracts import AbstractMenu
from bot.keyboards.default.menu import menu_kb
from bot.keyboards.inline import operator_faculties_ikb
from bot.states.machines import ChatFSM
from loader import dp

from bot.keyboards.default.chat import chat_kbs

from bot.states import MenuFSM
import bot.utils.http as http


async def flush_memory(state: FSMContext):
    await state.finish()


# OPEN FACULTY LIST
@dp.message_handler(text=menu_kb.Texts.chat.value, state=MenuFSM.main)
async def faculties(message: types.Message, state: FSMContext):
    await (await message.answer('Обработка...', reply_markup=types.ReplyKeyboardRemove())).delete()
    mes = await message.answer('Выберите тип оператора', reply_markup=operator_faculties_ikb.ikb)
    await state.update_data(faculties_message=mes)
    await state.set_state(ChatFSM.choosing_faculty)


# CLOSE FACULTY LIST --> MAIN MENU
@dp.callback_query_handler(text=operator_faculties_ikb.faculties_names_hashes[0], state=ChatFSM.choosing_faculty)
async def return_to_menu_with_call(call: types.CallbackQuery, state: FSMContext):
    await dp.bot.answer_callback_query(call.id)
    await end_ticket(call.message, state)
    
    await ((await state.get_data()).get('faculties_message')).delete()


# FACULTY IKB HANDLER --> QU INPUT
@dp.callback_query_handler(text=operator_faculties_ikb.faculties_hashes, state=ChatFSM.choosing_faculty)
async def get_qu(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Сформулируйте и напишите свой вопрос', reply_markup=chat_kbs.close_qu_kb)
    await dp.bot.answer_callback_query(call.id)
    
    faculties_message: types.Message = (await state.get_data()).get('faculties_message')
    await faculties_message.edit_reply_markup(None)
    await faculties_message.edit_text(text=operator_faculties_ikb.hash_to_name[call.data], reply_markup=None)
    await state.set_state(ChatFSM.writing_qu)
    await state.update_data(faculty_hash=call.data, faculties_message=None)


# CLOSE QU INPUT --> MAIN MENU
@dp.message_handler(text=chat_kbs.Texts.close_qu.value, state=ChatFSM.writing_qu)
async def return_to_menu_message(message: types.Message, state: FSMContext):
    await end_ticket(message, state)


# HANDLE QU INPUT --> QU APPLY
@dp.message_handler(state=ChatFSM.writing_qu)
async def set_qu(message: types.Message, state: FSMContext):
    await message.reply('Вы уверены в правильности вопроса?', reply_markup=chat_kbs.apply_chat_kb)
    await state.set_state(ChatFSM.apply_qu)
    await state.update_data(qu=message.text)


# CLOSE QU APPLY --> MAIN MENU
@dp.message_handler(text=chat_kbs.Texts.close_qu.value, state=ChatFSM.apply_qu)
async def close_qu(message: types.Message, state: FSMContext):
    await end_ticket(message, state)


# EDIT QU APPLY --> QU INPUT
@dp.message_handler(text=chat_kbs.Texts.discard_qu.value, state=ChatFSM.apply_qu)
async def edit_qu(message: types.Message, state: FSMContext):
    await message.answer('Сформулируйте и напишите свой вопрос', reply_markup=chat_kbs.close_qu_kb)
    await state.set_state(ChatFSM.writing_qu)


async def end_ticket(message: types.Message, state: FSMContext):
    await AbstractMenu.send(message)
    await state.set_state(MenuFSM.main)
    await flush_memory(state)


# APPLY QU APPLY --> CHAT
@dp.message_handler(text=chat_kbs.Texts.apply_qu.value, state=ChatFSM.apply_qu)
async def create_ticket(message: types.Message, state: FSMContext):
    waiting_message = await message.answer('Обработка...', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ChatFSM.waiting_chat)

    data = await state.get_data()
    qu_text = data.get('qu')
    faculty_hash = data.get('faculty_hash')
    
    ticket_id = uuid4().int
    # Запрос на апи для создания тикета
    res = await http.chat.send_ticket(
        message.from_user.id,
        ticket_id,
        qu_text,
        operator_faculties_ikb.hash_to_name[faculty_hash]
    )
    
    if res == 'err':
        await message.answer('Извините! Что-то пошло не так.\nПопробуйте ещё раз через минуту')
        await end_ticket(message, state)
        return
    
    await message.reply(
        'Ваша заявка отправлена, вам напишет первый освободившийся оператор, будьте терпеливы',
        reply_markup=menu_kb.kb
    )
    
    await end_ticket(message, state)
    async with state.proxy() as data:
        if 'tickets' in data:
            # TICKET FALSE --> WAITING | TRUE --> ACTIVE CHAT
            data['tickets'][ticket_id] = False
        else:
            data['tickets'] = {ticket_id: False}
            await state.finish()