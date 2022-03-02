from aiogram.dispatcher.filters.state import StatesGroup, State


class ShowItem(StatesGroup):
    ChooseType = State()
    ChooseCategory = State()
