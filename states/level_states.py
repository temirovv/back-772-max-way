from aiogram.fsm.state import State, StatesGroup


class BuyurtmaBerishState(StatesGroup):
    olib_ketish = State()
    yetkazib_berish = State()
    category = State()
    product = State()


class FiliallarState(StatesGroup):
    choose_filial = State()
