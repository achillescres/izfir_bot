from aiogram.dispatcher.filters.state import StatesGroup, State


class MainFSM(StatesGroup):
    choosing = State()
    choosed = State()
    waiting_chat = State()
    chat = State()
    nlp_qu = State


class NlpFSM(StatesGroup):
    writing = State()
    apply = State()
    hooking = State()
