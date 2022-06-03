from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    qus_list = State()
    qu_self = State()
