from aiogram import types

markup = types.InlineKeyboardMarkup(
    inline_keyboard=[[
        types.InlineKeyboardButton(text="Понятно", callback_data="agree")
    ]]
)
