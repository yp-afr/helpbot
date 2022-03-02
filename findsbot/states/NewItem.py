from aiogram.dispatcher.filters.state import StatesGroup, State


class NewItem(StatesGroup):
    CreateNew = State()
    ChooseType = State()
    ChooseCategory = State()
    EnterCaption = State()
    SetContact = State()
    AskForPhoto = State()
    WithPhoto = State()
    WithOutPhoto = State()
