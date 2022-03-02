from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeItem(StatesGroup):
    ChangeCaption = State()
    ChangePhoto = State()
