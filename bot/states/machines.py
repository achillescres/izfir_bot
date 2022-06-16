from aiogram.dispatcher.filters.state import StatesGroup, State


# Menu
class MenuFSM(StatesGroup):
    main = State()


# In chat
class ChatFSM(StatesGroup):
    choosing_faculty = State()
    waiting_chat = State()
    chat = State()
