import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEV_MODE = True if str(os.getenv('DEV_MODE')) == 'True' else False

PROJECT_ROOT = str(Path(__file__).parent.parent)
BOT_ROOT = PROJECT_ROOT + '/bot'

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
HOST_URL = str(os.getenv('HOST_URL'))

WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = HOST_URL + WEBHOOK_PATH

bot_admins = [
    487289925,
    740086487
]
