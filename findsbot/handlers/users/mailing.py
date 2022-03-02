import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from findsbot.filters import TextButton
from findsbot.keyboards.default.Administration import administration
from findsbot.keyboards.inline.mailing import mailing_cancel_keyboard, mailing_done_keyboard
from findsbot.loader import dp, bot
from findsbot.states.mailing_states import Mailing
from findsbot.utils.dp_api.commands import get_all_users


@dp.message_handler(TextButton("button_done"), state=Mailing.SendPhoto, admin_check=True)
async def mailing_done(message: types.Message, state: FSMContext):
    bot.parse_mode = ParseMode.MARKDOWN
    state_data = await state.get_data()
    await state.finish()
    markup = await administration()

    mailing_text = state_data.get("mailing_text")
    mailing_photo = state_data.get("mailing_photo")

    users = await get_all_users()
    it = 0
    await message.answer(f"Запускаю рассылку....", reply_markup=markup)
    if mailing_photo:
        for user in users:
            try:
                await bot.send_photo(chat_id=user, photo=mailing_photo, caption=mailing_text)
                it += 1
            except Exception as ex:
                logging.info(ex)
            await asyncio.sleep(0.4)

    else:
        for user in users:
            try:
                await bot.send_message(chat_id=user, text=mailing_text)
            except Exception as ex:
                logging.info(ex)
            await asyncio.sleep(0.4)
    await message.answer("Рассылка окончена!")
    bot.parse_mode = ParseMode.HTML


@dp.message_handler(TextButton("button_cancel_text"), state=Mailing)
async def mailing_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    markup = await administration()
    await message.answer("Успешно отменено", reply_markup=markup)


@dp.message_handler(TextButton("button_mailing"), admin_check=True)
async def do_mailing(message: types.Message):
    markup = await mailing_cancel_keyboard()
    await message.answer("<b>Новая рассылка</b>\n\nВведи текст: ", reply_markup=markup)
    await Mailing.EnterText.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=Mailing.EnterText, admin_check=True)
async def enter_mailing_text(message: types.Message, state: FSMContext):
    mailing_text = message.text
    markup = await mailing_done_keyboard()
    await message.answer("Отлично, теперь отправь фото", reply_markup=markup)
    await Mailing.SendPhoto.set()
    await state.update_data(mailing_text=mailing_text)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Mailing.SendPhoto, admin_check=True)
async def enter_mailing_photo(message: types.Message, state: FSMContext):
    mailing_photo = message.photo[-1].file_id
    await message.answer("Фото получено, нажми завершить для запуска рассылки")
    await Mailing.SendPhoto.set()
    await state.update_data(mailing_photo=mailing_photo)
