from aiogram.dispatcher.filters.state import StatesGroup, State


# Menu
class MenuFSM(StatesGroup):
    main = State()


# In chat
class ChatFSM(StatesGroup):
    choosing_faculty = State()
    writing_qu = State()
    apply_qu = State()
    waiting_chat = State()
    apply_chat = State()
    chat = State()
