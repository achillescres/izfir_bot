from io import BytesIO
from uuid import uuid4

from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ParseMode
from aiogram.utils.markdown import bold, text
from fastapi import FastAPI, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from bot.abstracts import AbstractMenu
from bot.abstracts.support import AbstractTicket
from bot.keyboards.default.chat import chat_kbs
from bot.states import ChatFSM, MenuFSM
from bot.utils.chat.utils import score_chat_with_bot
from bot.utils.divide_qus import *
from bot_app import TelegramBot
from data.config import WEBHOOK_PATH, WEBHOOK_URL, DEV_MODE, ACCESS_TOKEN
from server.models import *


app = FastAPI()
ibot = TelegramBot(dev=DEV_MODE)

origins = [
    '127.0.0.1'
    'http://127.0.0.1',
    'https://127.0.0.1'
    'http://85.193.89.20',
    'https://85.193.89.20'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def on_startup():
    await ibot.start(webhook_url=WEBHOOK_URL)


@app.on_event('shutdown')
async def on_shutdown():
    await ibot.shutdown()


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    await ibot.telegram_update(update)


# CHAT MODULE

@app.post('/bot/sendMessage')
async def bot_send_message(message: Message):
    state: FSMContext = ibot.dp.current_state(chat=message.user_id, user=message.user_id)
    await state.get_state()
    if (await state.get_state()) != ChatFSM.chat.state:
        logger.error('Tried to send message to user that isn\'t in chat')
        raise ValueError
    await ibot.send_message(text=message.text, user_id=message.user_id, operator_name=message.operator_name)


@app.post('/bot/sendFileMessage')
async def bot_send_file_message(file_type: str, file_name: str, user_id: str, file: UploadFile = File(...)):
    state: FSMContext = ibot.dp.current_state(chat=user_id, user=user_id)
    # print(state)
    # print((await state.get_state()))
    if (await state.get_state()) != ChatFSM.chat.state:
        logger.error('Tried to send message to user that isn\'t in chat')
        raise ValueError
    if file_type not in ['photo', 'video', 'document']:
        logger.error(f"Invalid file_type {file_type}")
        raise ValueError
    file_io = BytesIO(await file.read())

    file = InputFile(file_io, filename=file_name)
    
    match file_type:
        case 'photo':
            await ibot.bot.send_photo(chat_id=user_id, photo=file)
        case 'video':
            await ibot.bot.send_video(chat_id=user_id, video=file)
        case 'document':
            await ibot.bot.send_document(chat_id=user_id, document=file)


@app.post('/api/startChat')
async def start_chat(data: TicketAccept):
    state = ibot.dp.current_state(user=data.user_id, chat=data.user_id)
    async with state.proxy() as fsm_data_proxy:
        if (await state.get_state()) == ChatFSM.chat:
            return 'occupied'
        
        logger.info(f"Starting chat: {data.user_id} -> {data.chat_room_id}")
        await ibot.bot.send_message(
            text=text(
                r'Оператор откликнулся на ваш вопрос\! Начался чат\!\nЧтобы закрыть чат воспользуйтесь кнопкой или напишите',
                bold('/start'),
                r'\#свфуответ'
            ),
            chat_id=data.user_id,
            reply_markup=chat_kbs.finish_chat_kb,
            parse_mode=ParseMode.MARKDOWN_V2
        )
        
        await state.set_state(ChatFSM.chat)
        fsm_data_proxy['operator_id'] = data.chat_room_id
        fsm_data_proxy['operator_name'] = data.operator_name
        await AbstractTicket.flush_ticket_creation_data(state)
        await AbstractTicket.delete(state=state, ticket_id=data.chat_room_id)


@app.post("/api/finishChat")
async def finish_chat(user_id: UserId):
    await AbstractMenu.send_with_bot(bot=ibot.bot, user_id=user_id.user_id)
    
    client_state = ibot.dp.current_state(user=user_id.user_id, chat=user_id.user_id)
    await client_state.set_state(MenuFSM.main)
    
    try:
        await AbstractTicket.delete(
            state=client_state,
            ticket_id=user_id.chat_room_id,
            sync=False
        )
    except Exception as e:
        logger.error(e)
        logger.error("Can't delete ticket with AbstractTicket method")
    finally:
        await score_chat_with_bot(user_id.user_id, user_id.chat_room_id, ibot.bot)
        async with client_state.proxy() as fsm_data_proxy:
            if 'operator_name' in fsm_data_proxy:
                fsm_data_proxy.pop('operator_name')
            if 'operator_id' in fsm_data_proxy:
                fsm_data_proxy.pop('operator_id')


# FACULTIES MODULE

@app.get("/api/getFaculties/{fac_key}_{token}")
async def get_faculties(fac_key: str, token: str):
    if token != ACCESS_TOKEN:
        return 'invalid access token'

    if fac_key == 'all':
        return {
            'faculties': await ibot.data_proxy.collection.find(
                {},
                {"_id": 0, "qus_ans_calls": 0, "normal_qus_ans": 0}
            ).to_list(40)
        }

    return {
        'faculties': await ibot.data_proxy.collection.find(
            {"faculty.key": fac_key},
            {"_id": 0, "qus_ans_calls": 0, "normal_qus_ans": 0}
        ).to_list(40)
    }


@app.get("/api/getFaculty/{fac_key}_{token}")
async def get_faculty(fac_key: str, token: str):
    if token != ACCESS_TOKEN:
        return 'invalid access token'

    return {
        'faculties': await ibot.data_proxy.collection.find(
            {"faculty.key": fac_key},
            {"_id": 0, "qus_ans_calls": 0}
        ).to_list(40)
    }


@app.post("/api/setFaculty")
async def set_faculty(data: Facultie):
    data = jsonable_encoder(data)

    await ibot.data_proxy.collection.update_one(
        {'faculty.key': data["faculty_key"]},
        {'$set': {'normal_qus_ans': data["normal_qus_ans"]}}
    )
    
    rows = [[qu_an["qu"], qu_an["an"]] for qu_an in data["normal_qus_ans"]]

    await set_formatted_rows(ibot.data_proxy.collection, data["faculty_key"], rows)
    await ibot.update_question()


@app.post("/api/addFaculty")
async def add_faculty(data: AddFaculty):
    fac_key = str(uuid4())[:5]
    while await ibot.data_proxy.collection.find_one({"faculty.key": fac_key}):
        fac_key = str(uuid4())[:5]
    
    faculty = {
        "faculty": {
            "key": fac_key,
            "name": data.faculty_name
        },
        "qus_ans_calls": [],
        "normal_qus_ans": []
    }
    
    await ibot.data_proxy.collection.insert_one(faculty)
    await ibot.data_proxy.update_data()


# @app.post("api/")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host='localhost', port=8001)
