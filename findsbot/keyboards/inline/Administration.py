from aiogram import types

markup = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Назначить", callback_data="set_admin"),
     types.InlineKeyboardButton(text="Снять", callback_data="del_admin")],
    [types.InlineKeyboardButton(text="Список админов", callback_data="show_admins")]
])
