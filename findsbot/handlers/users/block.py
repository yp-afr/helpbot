from aiogram import types

from findsbot.loader import dp


@dp.message_handler(block_check=True)
async def block_users(message: types.Message):
    await message.answer("Вас заблоковано.", reply_markup=None)