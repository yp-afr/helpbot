from aiogram.types import ReplyKeyboardMarkup

from findsbot.utils.dp_api.commands import get_name


async def mailing_cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(await get_name("button_cancel_text"))
    return markup


async def mailing_done_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(await get_name("button_done"))
    markup.insert(await get_name("button_cancel_text"))
    return markup