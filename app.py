from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from bot.keyboards.default.chat import finish_chat_kb
from bot.states import MenuFSM
from bot.utils.divide_qus import *
from bot_app import IzfirBot
from data.config import WEBHOOK_PATH, WEBHOOK_URL, DEV_MODE
from server.models import Message, Facultie
from server.models import UserId

app = FastAPI()
ibot = IzfirBot(dev=DEV_MODE)

origins = [
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def on_startup():
    await ibot.start(WEBHOOK_URL=WEBHOOK_URL)


@app.on_event('shutdown')
async def on_shutdown():
    await ibot.shutdown()


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    await ibot.update(update)


@app.post('/bot/sendMessage')
async def bot_send_message(message: Message):
    await ibot.send_message(text=message.text, user_id=message.user_id, kb=finish_chat_kb.kb)


@app.post("/api/finishChat")
async def finish_chat(user_id: UserId):
    client_state = ibot.dp.current_state(user=user_id.user_id, chat=user_id.user_id)
    await client_state.set_state(MenuFSM.main)
    await ibot.send_message(
        text="Сеанс был завершен",
        user_id=user_id.user_id,
    )


@app.get("/api/getFaculties")
async def get_faculties():
    return {'faculties': await ibot.data_proxy.qus_ans_calls_collection.find({}, {"_id": 0, "qus_ans_calls": 0}).to_list(40)}


@app.post("/api/setFacultie")
async def set_facultie(data: Facultie):
    data = jsonable_encoder(data)
    await ibot.data_proxy.qus_ans_calls_collection.update_one(
        {'faculty.key': data["faculty_key"]}, {'$set': {'normal_qus_ans': data["normal_qus_ans"]}}
    )

    rows = [[qu_an["qu"], qu_an["an"]] for qu_an in data["normal_qus_ans"]]

    await format_rows(ibot.data_proxy.qus_ans_calls_collection, data["faculty_key"], rows)
    await ibot.data_proxy.update_data()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='localhost', port=8001, reload=True)
