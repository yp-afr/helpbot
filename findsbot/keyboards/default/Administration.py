from aiogram.types import ReplyKeyboardMarkup

from findsbot.utils.dp_api.commands import get_name


async def administration():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(await get_name("button_mailing"))
    markup.insert(await get_name("button_add_contact"))
    markup.insert(await get_name("button_all_contacts"))
    markup.insert(await get_name("button_add_info"))
    markup.insert(await get_name("button_show_blocked"))
    markup.row(await get_name("button_add_admin"))
    markup.insert(await get_name("button_show_list_of_admins"))
    markup.row(await get_name("button_back_to_main_menu"))
    return markup