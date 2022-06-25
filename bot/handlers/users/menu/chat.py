import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold, text

from bot.abstracts import AbstractMenu
from bot.keyboards.default.menu import menu_kb
from bot.keyboards.inline import operator_faculties_ikb
from bot.states.machines import ChatFSM
from loader import dp

from bot.keyboards.default.chat import chat_kbs

from bot.states import MenuFSM
import bot.utils.http as http


async def flush_memory(state: FSMContext):
    await state.update_data(faculties_message=None, qu=None, faculty_hash=None)


# Start
@dp.message_handler(text=menu_kb.Texts.chat.value, state=MenuFSM.main)
async def faculties(message: types.Message, state: FSMContext):
    mes = await message.answer('Обработка...', reply_markup=types.ReplyKeyboardRemove())
    await mes.delete()
    
    faculties_message = await message.answer('Выберите тип оператора', reply_markup=operator_faculties_ikb.ikb)
    await state.update_data(faculties_message=faculties_message)
    await state.set_state(ChatFSM.choosing_faculty)


# CLOSE FACULTY LIST --> MAIN MENU
@dp.callback_query_handler(text=operator_faculties_ikb.faculties_names_hashes[0], state=ChatFSM.choosing_faculty)
async def return_to_menu_with_call(call: types.CallbackQuery, state: FSMContext):
    await AbstractMenu.send(call)
    await dp.bot.answer_callback_query(call.id)
    await state.set_state(MenuFSM.main)

    await ((await state.get_data())['faculties_message']).delete()
    # CLEAN MEMORY
    await flush_memory(state)


# FACULTY IKB HANDLER --> QU INPUT
@dp.callback_query_handler(text=operator_faculties_ikb.faculties_hashes, state=ChatFSM.choosing_faculty)
async def get_qu(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Сформулируйте и напишите свой вопрос', reply_markup=chat_kbs.close_qu_kb)
    await dp.bot.answer_callback_query(call.id)
    
    await (await state.get_data())['faculties_message'].delete()
    await state.set_state(ChatFSM.writing_qu)
    await state.update_data(faculty_hash=call.data)


# CLOSE QU INPUT --> MAIN MENU
@dp.message_handler(text=chat_kbs.Texts.close_qu.value, state=ChatFSM.writing_qu)
async def return_to_menu_message(message: types.Message, state: FSMContext):
    await AbstractMenu.send(message)
    
    # CLEAN MEMORY
    await flush_memory(state)

    await state.set_state(MenuFSM.main)


# HANDLE QU INPUT --> QU APPLY
@dp.message_handler(state=ChatFSM.writing_qu)
async def set_qu(message: types.Message, state: FSMContext):
    await message.reply('Вы уверены в правильности вопроса?', reply_markup=chat_kbs.apply_chat_kb)
    await state.set_state(ChatFSM.apply_qu)
    await state.update_data(qu=message.text)


# CLOSE QU APPLY --> MAIN MENU
@dp.message_handler(text=chat_kbs.Texts.close_qu.value, state=ChatFSM.apply_qu)
async def close_qu(message: types.Message, state: FSMContext):
    await AbstractMenu.send(message)
    await state.set_state(MenuFSM.main)
    
    # CLEAN MEMORY
    await flush_memory(state)


# EDIT QU APPLY --> QU INPUT
@dp.message_handler(text=chat_kbs.Texts.discard_qu.value, state=ChatFSM.apply_qu)
async def edit_qu(message: types.Message, state: FSMContext):
    await message.answer('Сформулируйте и напишите свой вопрос', reply_markup=chat_kbs.close_qu_kb)
    await state.set_state(ChatFSM.writing_qu)


# APPLY QU APPLY --> CHAT
@dp.message_handler(text=chat_kbs.Texts.apply_qu.value, state=ChatFSM.apply_qu)
async def start_chat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    faculties_message = data['faculties_message']
    qu_text = data['qu']
    faculty_hash = data['faculty_hash']
    
    waiting_message = await message.answer('Идёт поиск оператора...', reply_markup=chat_kbs.finish_chat_kb)
    await state.set_state(ChatFSM.waiting_chat)

    # Запрос на апи для поиска оператора
    operator_id = await http.chat.get_operator(
        message.chat.id,
        operator_faculties_ikb.hash_to_name[faculty_hash]
    )

    logging.info(f'Found operator: {operator_id}')
    
    await waiting_message.delete()
    # Если нет свободного оператора
    if operator_id in ("null", ''):
        await message.answer('Извините! На данный момент все операторы заняты, либо отсутствуют.\nНапишите позже')
        await AbstractMenu.send(message)
        await state.set_state(MenuFSM.main)
        return

    await state.update_data(operator_id=operator_id, qu=None)
    
    await message.reply(
        'Оператор нашёлся! Чтобы завершить сеанс вы можете воспользоваться кнопкой или написать /start',
        reply_markup=chat_kbs.finish_chat_kb
    )
    
    sent = await http.chat.produce_message(
        user_id=message.from_user.id,
        operator_id=operator_id,
        message=qu_text
    )
    
    # If couldn't send
    if sent == 'err':
        logging.info(f"Couldn't send message to operator: {operator_id} from user: {message.from_user.id}")
        await close_chat(message, state, from_user=True, with_err=True)
        return
    
    await state.set_state(ChatFSM.chat)


@dp.message_handler(state=ChatFSM.choosing_faculty)
async def choosing_operator_faculty_trash(message: types.Message):
    await message.reply('Пожалуйста воспользуйтесь кнопками, чтобы выбрать тип оператора')


@dp.message_handler(text='/Завершить сеанс', state=MenuFSM.main)
async def finish_chat_trash(message: types.Message):
    await AbstractMenu.send(message)


@dp.message_handler(state=ChatFSM.waiting_chat)
async def waiting_chat_trash(message: types.Message):
    await message.reply('Подождите конца поиска оператора, или нажмите кнопку')


# Universal function to close_chat, closing user-side and operator-side
async def close_chat(message: types.Message, state: FSMContext, from_user=True, with_err=False):
    if from_user:
        operator_id = (await state.get_data()).get('operator_id')

        canceled = await http.chat.cancel(operator_id=operator_id, user_id=message.from_user.id)
        if canceled == 'err' or with_err:
            await message.answer(
                text=text(
                    'Наблюдаются проблемы с подключением к операторам, если вы не сможете подключиться снова попробуйте написать ',
                    bold('/start'),
                ),
                parse_mode=ParseMode.MARKDOWN_V2
            )

    await message.answer('Cеанс завершен', reply_markup=menu_kb.kb)
    await state.update_data(operator_id=None)
    await state.set_state(MenuFSM.main)


# Close on keyboard close button
@dp.message_handler(text=[chat_kbs.Texts.finish_chat.value, '/start'], state=[ChatFSM.chat, ChatFSM.waiting_chat])
async def close_support(message: types.Message, state: FSMContext):
    await close_chat(message, state, from_user=True, with_err=False)


@dp.message_handler(state=ChatFSM.chat, content_types=['photo'])
async def handle_docs_photo(message):
    await message.photo[-1].download(destination_file='test.jpg')


# Send message from user
@dp.message_handler(state=ChatFSM.chat)
async def send_support(message: types.Message, state: FSMContext):
    operator_id = (await state.get_data()).get('operator_id')
    logging.info(f'Sending message to operator: {operator_id} from user: {message.from_user.id}')

    # If haven't operator_id in FSM
    if not operator_id:
        logging.info(f'HAVE NOT OPERATOR_ID IN FSM! CLOSING_CHAT FOR USER: {message.from_user.id}')
        await close_chat(message, state, from_user=True, with_err=True)
        return

    logging.info(f'Sending message to {operator_id}')
    # Send message to site api(http library always makes 3 attempts)
    sent = await http.chat.produce_message(
        user_id=message.from_user.id,
        operator_id=operator_id,
        message=message.text
    )

    # If couldn't send
    if sent == 'err':
        logging.info(f"Couldn't send message to operator: {operator_id} from user: {message.from_user.id}")
        await close_chat(message, state, from_user=True, with_err=True)
