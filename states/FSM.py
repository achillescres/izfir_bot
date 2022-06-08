from aiogram.dispatcher.filters.state import StatesGroup, State


class FSM(StatesGroup):
    choosing = State()
    choosed = State()
    waiting_chat = State()
    chat = State()
