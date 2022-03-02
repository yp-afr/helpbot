from aiogram.dispatcher.filters.state import StatesGroup, State


class AddingContact(StatesGroup):
    EnterContact = State()
