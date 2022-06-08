from fastapi import FastAPI
from bot_app import IzfirBot
from bot.data.config import WEBHOOK_PATH, WEBHOOK_URL
from manager.models import Message

app = FastAPI()
ibot = IzfirBot()


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
    await ibot.send_message(text=message.text, user_id=message.user_id)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='localhost', port=8000, reload=True)
