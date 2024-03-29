import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEV_MODE = True if str(os.getenv('DEV_MODE')) == 'True' else False

PROJECT_ROOT = str(Path(__file__).parent.parent)
BOT_ROOT = PROJECT_ROOT + '/bot'

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
HOST_URL = str(os.getenv('HOST_URL'))
ACCESS_TOKEN = str(os.getenv('ACCESS_TOKEN'))

WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = HOST_URL + WEBHOOK_PATH

bot_admins = [
    487289925,
    740086487
]

SERVER_URL = str(os.getenv('SERVER_URL'))
SERVER_API = SERVER_URL + '/api'

# ANTI-FLOOD
DEFAULT_RATE_LIMIT = float(os.getenv('DEFAULT_RATE_LIMIT')) or .3
DEFAULT_SPAM_STUN = float(os.getenv('DEFAULT_SPAM_STUN')) or 2.5