from fastapi import FastAPI
from bot_app import IzfirBot
from data.config import WEBHOOK_PATH, WEBHOOK_URL

app = FastAPI()
ibot = IzfirBot()


@app.on_event('startup')
async def on_startup():
    await ibot.start(WEBHOOK_URL=WEBHOOK_URL)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    await ibot.update(update)


@app.on_event('shutdown')
async def on_shutdown():
    await ibot.shutdown()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='localhost', port=8000, reload=True)
