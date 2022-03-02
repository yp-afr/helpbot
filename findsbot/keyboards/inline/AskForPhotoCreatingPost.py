from aiogram import types

markup = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Так", callback_data="yes"),
     types.InlineKeyboardButton(text="Ні", callback_data="no")]
])
