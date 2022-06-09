from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bot_app import IzfirBot
from bot.data.config import WEBHOOK_PATH, WEBHOOK_URL
from manager.models import Message

app = FastAPI()
ibot = IzfirBot()

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
async def send_message(message: Message):
    print(123456)
    print(message.text)
    await ibot.send_message(text=message.text, user_id=message.user_id)


@app.get("/api/finishChat/{client_id}")
async def finish_chat(client_id: str):
    client_state = ibot.dp.current_state(user=client_id, chat=client_id)
    await client_state.set_state(None)
    await ibot.send_message(text="Сеанс был завершен", user_id=client_id)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='localhost', port=8001, reload=True)
