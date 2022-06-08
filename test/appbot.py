from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from aiobot import dp, bot, API_TOKEN

app = FastAPI()
WEBHOOK_PATH = f"/bot/{API_TOKEN}"
WEBHOOK_URL = "https://f629-94-245-129-108.jp.ngrok.io" + WEBHOOK_PATH


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post('/123')
async def ybot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)
    return 'lol'


@app.post('/bot/5548062448AAGoAK02:eNB3aXRdEPN10hSzkpbfgGSqjUI')
async def bot_webhook(update: dict):
    pass


@app.get("/api/finishChat/{client_id}")
async def finishChat(client_id: str):
    client_state = dp.current_state(user=client_id, chat=client_id)
    await client_state.set_state(None)
    await dp.bot.send_message(client_id, "Сеанс был завершен")


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
