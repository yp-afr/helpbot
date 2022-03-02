from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from findsbot.keyboards.default.main_menus import main_menu, admin_main_menu
from findsbot.loader import dp
from findsbot.utils.dp_api import commands
from findsbot.utils.dp_api.commands import get_name


@dp.message_handler(CommandStart(), state='*', admin_check=True)
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    markup = await admin_main_menu()
    await message.answer(text=await get_name("subscribed_message"), reply_markup=markup)
    user_id = message.from_user.id
    await commands.add_user(user_id)


@dp.message_handler(CommandStart(), state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    markup = await main_menu()
    await message.answer(text=await get_name("subscribed_message"), reply_markup=markup)