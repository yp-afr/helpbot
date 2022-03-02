from aiogram import types
from aiogram.dispatcher.filters import Filter

from findsbot.utils.dp_api.commands import get_name


class TextButton(Filter):
    key = "text_button"

    def __init__(self, button_code: str):
        self.button_code: str = button_code

    async def check(self, message: types.Message) -> bool:
        name = await get_name(self.button_code)
        return message.text == name
