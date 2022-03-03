import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from findsbot.filters import TextButton
from findsbot.keyboards.default.Administration import administration
from findsbot.keyboards.default.main_menus import admin_main_menu
from findsbot.keyboards.inline.administration_funcs import contact_keyboard, new_admin_keyboard, delete_admin_cd, \
    tr_contact_keyboard, delete_contact_cd, blocked_key
from findsbot.loader import dp, bot
from findsbot.states.AddContact import AddingContact
from findsbot.states.AddInfo import AddingInfo
from findsbot.states.AddingAdmin import AddingAdmin
from findsbot.utils.dp_api.commands import get_all_admins, add_admin, del_admin, get_name, add_contactt, \
    get_all_contacts, delete_contact, add_iinfo, get_blocked, get_all_users


@dp.message_handler(TextButton("button_admin_text"), admin_check=True)
async def admin(message: types.Message):
    markup = await administration()
    await message.answer("Меню администратора: ", reply_markup=markup)


@dp.message_handler(TextButton("button_back_to_main_menu"))
async def go_back_to_main_menu(message: types.Message):
    markup = await admin_main_menu()
    await message.answer(text=await get_name("menu_text"), reply_markup=markup)


@dp.message_handler(TextButton("button_show_list_of_admins"), admin_check=True)
async def show_admins(message: types.Message):
    admins = await get_all_admins()
    if admins:
        for adm in admins:
            try:
                markup = await contact_keyboard(adm.phone_number)
                await message.answer_contact(adm.phone_number, adm.first_name, reply_markup=markup)
            except Exception as ex:
                logging.error(ex)
    else:
        await message.answer("Список назначенных админов пуст!")


@dp.message_handler(TextButton("button_cancel_text"), state="*", admin_check=True)
async def cancel_adding(message: types.Message, state: FSMContext):
    await state.finish()
    markup = await administration()
    await message.answer("Скасовано!", reply_markup=markup)


@dp.message_handler(TextButton("button_add_info"), admin_check=True)
async def add_info(message: types.Message):
    markup = await new_admin_keyboard()
    await message.answer("Введіть інформацію (вона має виглядати як звичайний пост в каналі)", reply_markup=markup)
    await AddingInfo.EnterInfo.set()


@dp.message_handler(content_types=types.ContentType.TEXT, admin_check=True, state=AddingInfo.EnterInfo)
async def enter_info_text(message: types.Message, state: FSMContext):
    try:
        await add_iinfo(info=message.text)
        markup = await administration()
        await message.answer("Інформація додана!", reply_markup=markup)
        users = await get_all_users()
        it = 0
        await message.answer(f"Запускаю рассылку....", reply_markup=markup)

        for user in users:
            try:
                await bot.send_message(chat_id=user, text=message.text)
                it += 1
            except Exception as ex:
                logging.info(ex)
            await asyncio.sleep(0.4)
    except Exception as ex:
        markup = await administration()
        await message.answer(f"Помилка додавання!", reply_markup=markup)
        logging.error(ex)
    await state.finish()


@dp.message_handler(TextButton("button_add_contact"), admin_check=True)
async def add_contact(message: types.Message):
    markup = await new_admin_keyboard()
    await message.answer("Введіть перевірений контакт у форматі @contact_username", reply_markup=markup)
    await AddingContact.EnterContact.set()


@dp.message_handler(content_types=types.ContentType.TEXT, admin_check=True, state=AddingContact.EnterContact)
async def enter_contact_text(message: types.Message, state: FSMContext):
    try:
        await add_contactt(contact=message.text)
        markup = await administration()
        await message.answer("Контакт додано!", reply_markup=markup)
    except Exception as ex:
        markup = await administration()
        await message.answer(f"Помилка додавання!", reply_markup=markup)
        logging.error(ex)
    await state.finish()


@dp.message_handler(TextButton('button_all_contacts'), admin_check=True)
async def show_all_contacts(message: types.Message, state: FSMContext):
    try:
        contacts = await get_all_contacts()
        if contacts:
            for c in contacts:
                markup = await tr_contact_keyboard(c.id)
                await message.answer(c.name, reply_markup=markup)
        else:
            await message.answer('Контакти відсутні')
    except Exception as ex:
        markup = await administration()
        await message.answer(f"Помилка виконання!", reply_markup=markup)
        logging.error(ex)


@dp.message_handler(TextButton("button_add_admin"), admin_check=True)
async def add_administrator(message: types.Message):
    markup = await new_admin_keyboard()
    await message.answer("""Для добавления администратора необходимо отправить его контакт
(📎 -> Контакт)""", reply_markup=markup)
    await AddingAdmin.SendContact.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=AddingAdmin.SendContact)
async def getting_contact(message: types.Message, state: FSMContext):
    try:
        await add_admin(phone=message.contact.phone_number, first_name=message.contact.first_name,
                        admin_id=str(message.contact.user_id))
        markup = await administration()
        await message.answer("Новый администратор успешно добавлен!", reply_markup=markup)
    except Exception as ex:
        markup = await administration()
        await message.answer(f"Ошибка добавления!", reply_markup=markup)
        logging.error(ex)
    await state.finish()


@dp.message_handler(TextButton('button_show_blocked'))
async def show_all_blocked(message: types.Message):
    try:
        blocked = await get_blocked()
        if blocked:
            for b in blocked:
                markup = await blocked_key(b.id)
                await message.answer(b.name, reply_markup=markup)
        else:
            await message.answer('Заблоковані відсутні')
    except Exception as ex:
        markup = await administration()
        await message.answer(f"Помилка виконання!", reply_markup=markup)
        logging.error(ex)


@dp.callback_query_handler(delete_admin_cd.filter())
async def deleting_admin(call: types.CallbackQuery, callback_data: dict):
    phone = callback_data.get("phone_number")
    await del_admin(phone)
    await call.message.delete()


@dp.callback_query_handler(delete_contact_cd.filter())
async def deleting_contact(call: types.CallbackQuery, callback_data: dict):
    id = callback_data.get("id")
    await delete_contact(id)
    await call.message.delete()
