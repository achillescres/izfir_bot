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

from bot.keyboards.default.chat import finish_chat_kb

from bot.states import MenuFSM
import bot.utils.http as http


@dp.message_handler(text=menu_kb.Texts.chat.value, state=MenuFSM.main)
async def choose_operator_faculty(message: types.Message, state: FSMContext):
    await message.answer('Выберите тип оператора', reply_markup=operator_faculties_ikb.ikb)
    await state.set_state(ChatFSM.choosing_faculty)


@dp.callback_query_handler(text=operator_faculties_ikb.faculties_names_hashes[0], state=ChatFSM.choosing_faculty)
async def return_to_menu(call: types.CallbackQuery, state: FSMContext):
    await dp.bot.answer_callback_query(call.id)
    await call.message.answer(menu_kb.self_text, reply_markup=menu_kb.kb)
    await call.message.delete()
    await state.set_state(MenuFSM.main)


# Start chat from main menu chat button startpoint
@dp.callback_query_handler(text=operator_faculties_ikb.faculties_hashes, state=ChatFSM.choosing_faculty)
async def start_chat(call: types.CallbackQuery, state: FSMContext):
    await dp.bot.answer_callback_query(call.id)
    await call.message.delete_reply_markup()
    await call.message.edit_text(operator_faculties_ikb.hash_to_name[call.data])
    waiter_message = await call.message.answer('Идёт поиск оператора...', reply_markup=finish_chat_kb.kb)
    await state.set_state(ChatFSM.waiting_chat)

    # Запрос на апи для поиска оператора
    operator_id = await http.chat.get_operator(
        call.message.chat.id,
        operator_faculties_ikb.hash_to_name[call.data]
    )

    logging.info(f'Found operator: {operator_id}')

    # Если нет свободного оператора
    if operator_id in ("null", ''):
        await waiter_message.delete()
        await call.message.answer('Извините! На данный момент все операторы заняты, либо отсутствуют.\nНапишите позже')
        await AbstractMenu.send(call.message)
        await state.set_state(MenuFSM.main)
        return

    await call.message.reply(
        'Оператор нашёлся! Чтобы завершить сеанс вы можете воспользоваться кнопкой или написать /start ',
        reply_markup=finish_chat_kb.kb
    )
    await state.update_data(operator_id=operator_id)
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
@dp.message_handler(text=[finish_chat_kb.Texts.close.value, '/start'], state=[ChatFSM.chat, ChatFSM.waiting_chat])
async def close_support(message: types.Message, state: FSMContext):
    await close_chat(message, state, from_user=True, with_err=False)


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
