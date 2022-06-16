from aiogram.dispatcher.filters.state import StatesGroup, State


# Menu
class MenuFSM(StatesGroup):
    main = State()


# In chat
class ChatFSM(StatesGroup):
    waiting_chat = State()
    chat = State()
