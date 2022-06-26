@dp.message_handler(state=ChatFSM.choosing_faculty)
async def choosing_operator_faculty_trash(message: types.Message):
	await message.reply('Пожалуйста воспользуйтесь кнопками, чтобы выбрать тип оператора')


@dp.message_handler(text='/Завершить сеанс', state=MenuFSM.main)
async def finish_chat_trash(message: types.Message):
	await AbstractMenu.send(message)


@dp.message_handler(state=ChatFSM.waiting_chat)
async def waiting_chat_trash(message: types.Message):
	await message.reply('Подождите конца поиска оператора, или нажмите кнопку')


# await message.answer(
#                 text=text(
#                     'Наблюдаются проблемы с сервисом, если вы не сможете подключиться снова попробуйте написать',
#                     bold('/start'),
#                     'или подождать несколько минут'
#                 ),
#                 parse_mode=ParseMode.MARKDOWN_V2
#             )


# Universal function to close_chat, closing user-side and operator-side
async def close_chat(message: types.Message, state: FSMContext, from_user=True, with_err=False):
	if from_user:
		operator_id = (await state.get_data()).get('operator_id')
		
		canceled = await http.chat.cancel(operator_id=operator_id, user_id=message.from_user.id)
		if canceled == 'err' or with_err:
			logging.info('Error with canceling chat')
			await http.chat.cancel(operator_id=operator_id, user_id=message.from_user.id)
		
		await message.answer('Cеанс завершен', reply_markup=menu_kb.kb)
	
	await flush_memory(state, operator_id=None)
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
async def send_message(message: types.Message, state: FSMContext):
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
