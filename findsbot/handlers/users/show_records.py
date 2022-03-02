import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from findsbot.filters import TextButton
from findsbot.handlers.users.callbacks import change_post_cb, del_post
from findsbot.keyboards.inline.administration_funcs import info_keyboard, delete_info_cd
from findsbot.keyboards.inline.types_categories import types_cd, categories_keyboard, types_keyboard, categories_cd
from findsbot.loader import dp
from findsbot.utils.dp_api.commands import get_records, get_admins, get_name, get_all_contacts, get_info, delete_info


@dp.message_handler(TextButton("button_allposts_text"))
async def show_items(message: types.Message):
    markup = await types_keyboard()
    await message.answer(text=await get_name("choose_type_text_all"), reply_markup=markup)


@dp.callback_query_handler(types_cd.filter())
async def show_all_choose_type(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    type_finds = callback_data.get("value")
    markup = await categories_keyboard()
    await call.message.edit_text(text=await get_name("choose_categorie_text"), reply_markup=markup)
    await state.update_data(item_type=type_finds)


@dp.callback_query_handler(categories_cd.filter(value="Назад"))
async def back_to_types(call: types.CallbackQuery):
    markup = await types_keyboard()
    await call.message.delete()
    await call.message.answer(text=await get_name("choose_type_text_all"), reply_markup=markup)


@dp.callback_query_handler(categories_cd.filter())
async def show_all_choose_category(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    category = callback_data.get("value")
    data = await state.get_data()
    item_type = data.get("item_type")
    await call.message.delete()
    rows = await get_records(type_finds=item_type, category=category)
    if rows:
        for row in rows:
            admins = await get_admins()
            if int(types.User.get_current().id) in admins:
                markup = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text="Изменить",
                                                callback_data=change_post_cb.new(item_id=int(row.id))),
                     types.InlineKeyboardButton(text="Удалить", callback_data=del_post.new(item_id=int(row.id)))]
                ])
            else:
                markup = None
            contacts = await get_all_contacts()
            if row.author_username:
                for contact in contacts:
                    if str(row.author_username) == str(contact.name):
                        row.author_username += "\n\n<i><b>Перевірений користувач</b></i>"
                        break

            if row.photo is None:
                await call.message.answer(f"<b>{row.type}</b> -- {row.category}\n\n{row.caption}\n"
                                          f"\nКонтакти: {row.author_username}", reply_markup=markup)
            else:
                await call.message.answer_photo(photo=row.photo,
                                                caption=f"<b>{row.type}</b> -- {row.category}\n\n{row.caption}"
                                                        f"\n\nКонтакти: {row.author_username}", reply_markup=markup)
            await asyncio.sleep(0.3)
    else:
        await call.message.answer(f"Категорія <b>{item_type}->{category}</b> порожня")
    await state.reset_state()


@dp.message_handler(TextButton("button_info"))
async def show_info(message: types.Message):
    info = await get_info()
    if info:
        admins = await get_admins()
        for i in info:
            if int(types.User.get_current().id) in admins:
                markup = await info_keyboard(i.id)
                await message.answer(i.name, reply_markup=markup)
            else:
                await message.answer(i.name)
    else:
        await message.answer("Інформація відсутня")


@dp.callback_query_handler(delete_info_cd.filter())
async def deleting_contact(call: types.CallbackQuery, callback_data: dict):
    id = callback_data.get("id")
    await delete_info(id)
    await call.message.delete()
