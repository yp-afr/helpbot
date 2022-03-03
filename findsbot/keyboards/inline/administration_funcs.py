from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from findsbot.handlers.users.callbacks import del_block
from findsbot.utils.dp_api.commands import get_name

delete_admin_cd = CallbackData("del_admin", "phone_number")
delete_contact_cd = CallbackData("del_con", "id")
delete_info_cd = CallbackData("del_info", "id")


async def tr_contact_keyboard(id):
    markup = InlineKeyboardMarkup()
    markup.insert(InlineKeyboardButton(text="Видалити", callback_data=delete_contact_cd.new(id=id)))
    return markup


async def blocked_key(id):
    markup = InlineKeyboardMarkup()
    markup.insert(InlineKeyboardButton(text="Видалити", callback_data=del_block.new(blocked_id=id)))
    return markup


async def info_keyboard(id):
    markup = InlineKeyboardMarkup()
    markup.insert(InlineKeyboardButton(text="Видалити", callback_data=delete_info_cd.new(id=id)))
    return markup


async def contact_keyboard(phone_number):
    markup = InlineKeyboardMarkup()
    markup.insert(InlineKeyboardButton(text="Снять", callback_data=delete_admin_cd.new(phone_number=phone_number)))
    return markup


async def new_admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(await get_name("button_cancel_text"))
    return markup
