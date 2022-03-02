from aiogram import types

from findsbot.utils.dp_api.commands import get_name


async def cancel():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(await get_name("button_cancel_text"))
    return markup
