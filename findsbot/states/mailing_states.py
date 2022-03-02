from aiogram.dispatcher.filters.state import StatesGroup, State


class Mailing(StatesGroup):
    EnterText = State()
    SendPhoto = State()