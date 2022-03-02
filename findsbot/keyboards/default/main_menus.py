from aiogram import types

from findsbot.utils.dp_api.commands import get_name


async def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(await get_name("button_create_text"), await get_name("button_myposts_text"))
    markup.add(await get_name("button_allposts_text"), await get_name("button_info"))
    return markup


async def admin_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(await get_name("button_create_text"), await get_name("button_myposts_text"))
    markup.add(await get_name("button_allposts_text"), await get_name("button_info"))
    markup.row(await get_name("button_admin_text"))
    return markup
