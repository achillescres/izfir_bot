import asyncio
from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import bold, text
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, File
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from bot.abstracts import AbstractMenu
from bot.abstracts.support import AbstractTicket
from bot.handlers.users.menu.support.ticket.ticket import flush_ticket_creation_data
from bot.keyboards.default.chat import chat_kbs
from bot.states import MenuFSM, ChatFSM
from bot.utils.divide_qus import *
from bot.utils.misc import remove_kb
from bot_app import TelegramBot
from data.config import WEBHOOK_PATH, WEBHOOK_URL, DEV_MODE, ACCESS_TOKEN
from server.models import Message, Facultie
from server.models import UserId, TicketAccept

scheduler = AsyncIOScheduler()
scheduler.start()

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
    allow_origins=origins,
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
    await ibot.update(update)


# CHAT MODULE

@app.post('/bot/sendMessage')
async def bot_send_message(message: Message):
    await ibot.send_message(text=message.text, user_id=message.user_id, operator_name=message.operator_name)


@app.post('/bot/sendFilesMessages/{file_type}/{file_name}/{user_id}')
async def bet_send_file_message(file_type: str, user_id: str, file: bytes = File(...)):
    if file_type not in ['photo', 'video', 'document']:
        return 'err'
    # types.InputFile(file, )
    await ibot.bot.send_file(file_type=file_type, file=file)
    await ibot.bot.send_file()


async def cancel_chat(message: types.Message, state: FSMContext):
    await message.edit_reply_markup(None)
    await message.reply(
        'Заявка была отклонена, потому что вы не приняли его в течении 10 минут'
    )
    await AbstractMenu.send(message)
    await state.set_state(MenuFSM.main)


@app.post('/api/startChat')
async def start_chat(data: TicketAccept):
    state = ibot.dp.current_state(user=data.user_id, chat=data.user_id)
    async with state.proxy() as fsm_data_proxy:
        if (await state.get_state()) == ChatFSM.chat:
            return 'occupied'
        
        await ibot.bot.send_message(
            text=text(
                'Оператор откликнулся на ваш вопрос!\nЧтобы закрыть чат воспользуйтесь кнопкой или напишите',
                bold('/start')
            ),
            chat_id=data.user_id,
            reply_markup=chat_kbs.finish_chat_kb,
        )
        
        await state.set_state(ChatFSM.chat)
        fsm_data_proxy['operator_id'] = data.operator_id
        fsm_data_proxy['operator_name'] = data.operator_name
        await flush_ticket_creation_data(state)
        await AbstractTicket.delete(state=state, ticket_id=data.ticket_id)


@app.post("/api/finishChat")
async def finish_chat(user_id: UserId):
    await ibot.send_message(
        text="Сеанс был завершен",
        user_id=user_id.user_id,
    )
    
    client_state = ibot.dp.current_state(user=user_id.user_id, chat=user_id.user_id)
    await AbstractTicket.delete(
        state=client_state
    )

    await client_state.reset_state(with_data=False)


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

    await format_rows(ibot.data_proxy.collection, data["faculty_key"], rows)
    await ibot.data_proxy.update_data()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host='localhost', port=8001)
