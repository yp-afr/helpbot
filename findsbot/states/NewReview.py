from aiogram.dispatcher.filters.state import StatesGroup, State


class NewReview(StatesGroup):
    AskQuestion = State()
    EnterCaption = State()
