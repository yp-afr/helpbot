from aiogram import types

markup = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text="ะขะฐะบ ๐", callback_data="yes_review"),
         types.InlineKeyboardButton(text="ะั ๐", callback_data="no_review")]
    ]
)