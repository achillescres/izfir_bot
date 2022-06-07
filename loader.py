from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config


# Create bot
from utils.load_qus_ans import load_qus_ans

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

# Create dispatcher
dp = Dispatcher(bot, storage=MemoryStorage())  # File end-point

# Get qus_ans
qus_ans_calls = load_qus_ans()
print(qus_ans_calls)
calls_to_ans = {call: an for (qu, an, call) in qus_ans_calls}
