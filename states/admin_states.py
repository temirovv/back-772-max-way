from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    add_category = State()
    add_vacancy = State()


class AddProductState(StatesGroup):
    category = State()
    name = State()
    description = State()
    price = State()
    image = State()

