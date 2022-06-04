from aiogram.dispatcher.filters.state import StatesGroup, State


class Fsm(StatesGroup):
    main = State()
    qus_list = State()
    qu_self = State()
