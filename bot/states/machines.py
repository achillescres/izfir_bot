from aiogram.dispatcher.filters.state import StatesGroup, State


# Registration
class RegFSM(StatesGroup):
    education_type = State()
    faculty = State()


# Menu
class MenuFSM(StatesGroup):
    main = State()
    qus_ans = State()


# In chat
class ChatFSM(StatesGroup):
    waiting_chat = State()
    chat = State()


# In nlp
class NlpFSM(StatesGroup):
    writing = State()
    apply = State()
    hooking = State()
