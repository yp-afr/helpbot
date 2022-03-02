from aiogram import types
from aiogram.utils.callback_data import CallbackData

from findsbot.utils.dp_api.commands import get_name

types_cd = CallbackData("type", "value")
categories_cd = CallbackData("category", "value")
new_post_types_cd = CallbackData("type", "value")


async def categories_keyboard():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=await get_name("button_drugs"), callback_data=categories_cd.new("Ліки"))],
        [types.InlineKeyboardButton(text=await get_name("button_eat"), callback_data=categories_cd.new("Їжа"))],
        [types.InlineKeyboardButton(text=await get_name("button_soap"), callback_data=categories_cd.new("Засоби гігієни"))],
        [types.InlineKeyboardButton(text=await get_name("button_house"), callback_data=categories_cd.new("Житло"))],
        [types.InlineKeyboardButton(text=await get_name("button_car"), callback_data=categories_cd.new("Підвезти"))],
        [types.InlineKeyboardButton(text=await get_name("button_family"), callback_data=categories_cd.new("Шукаю близьких"))],
        [types.InlineKeyboardButton(text=await get_name("button_pets"), callback_data=categories_cd.new("Допомога тваринам"))],
        [types.InlineKeyboardButton(text=await get_name("button_else"), callback_data=categories_cd.new("Інша допомога"))],
        [types.InlineKeyboardButton(text=await get_name("button_back"), callback_data=categories_cd.new("Назад"))],
    ])
    return markup


async def types_keyboard():
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=await get_name("button_found"),
                                        callback_data=types_cd.new(await get_name("button_found"))),
             types.InlineKeyboardButton(text=await get_name("button_lost"),
                                        callback_data=types_cd.new(await get_name("button_lost")))]
        ]
    )
    return markup


async def new_post_types_keyboard():
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=await get_name("button_finds"),
                                        callback_data=new_post_types_cd.new(await get_name("button_found"))),
             types.InlineKeyboardButton(text=await get_name("button_losts"),
                                        callback_data=new_post_types_cd.new(await get_name("button_lost")))]
        ]
    )
    return markup