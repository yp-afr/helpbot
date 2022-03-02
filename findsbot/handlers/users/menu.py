from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BadRequest

from findsbot.keyboards.default.main_menus import main_menu, admin_main_menu
from findsbot.loader import dp, bot
from findsbot.utils.dp_api.commands import get_name


@dp.message_handler(commands="menu", state='*', admin_check=True)
async def menu(message: types.Message, state: FSMContext):
    await state.reset_state()
    user_id = message.from_user.id
    chat_id = "@lovechernihiv"
    try:
        result = await bot.get_chat_member(chat_id, user_id)
        if result['status'] == 'left':
            await message.answer(text=await get_name("unsubscribed_message"), reply_markup=None)
        else:
            markup = await admin_main_menu()
            await message.answer(text=await get_name("subscribed_message"), reply_markup=markup)
    except BadRequest:
        await message.answer(text=await get_name("unsubscribed_message"), reply_markup=None)


@dp.message_handler(commands="menu", state='*')
async def menu(message: types.Message, state: FSMContext):
    await state.reset_state()
    user_id = message.from_user.id
    chat_id = "@lovechernihiv"
    try:
        result = await bot.get_chat_member(chat_id, user_id)
        if result['status'] == 'left':
            await message.answer(text=await get_name("unsubscribed_message"), reply_markup=None)
        else:
            markup = await main_menu()
            await message.answer(text=await get_name("subscribed_message"), reply_markup=markup)
    except BadRequest:
        await message.answer(text=await get_name("unsubscribed_message"), reply_markup=None)
