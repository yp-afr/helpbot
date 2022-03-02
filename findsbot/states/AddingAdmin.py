from aiogram.dispatcher.filters.state import StatesGroup, State


class AddingAdmin(StatesGroup):
    SendContact = State()
