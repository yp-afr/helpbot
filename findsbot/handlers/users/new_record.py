from aiogram import types
from aiogram.dispatcher import FSMContext

from findsbot.filters import TextButton
from findsbot.keyboards.default.Cancel import cancel
from findsbot.keyboards.default.main_menus import main_menu, admin_main_menu
from findsbot.keyboards.inline import BankInfoAgree, \
    AskForPhotoCreatingPost
from findsbot.keyboards.inline.types_categories import categories_keyboard, new_post_types_keyboard, new_post_types_cd, \
    categories_cd
from findsbot.loader import dp
from findsbot.states.NewItem import NewItem
from findsbot.utils.dp_api.commands import add_new_record, get_admins, get_name, get_all_contacts
from findsbot.utils.misc.mailing import mailing
from findsbot.utils.misc.moderation import moderation


@dp.message_handler(TextButton("button_cancel_text"), state=NewItem, admin_check=True)
async def check(message: types.Message, state: FSMContext):
    markup = await admin_main_menu()
    await message.answer(text=await get_name("creating_post_canceled_text"), reply_markup=markup)
    await state.reset_state()


@dp.message_handler(TextButton("button_cancel_text"), state=NewItem)
async def check(message: types.Message, state: FSMContext):
    markup = await main_menu()
    await message.answer(text=await get_name("creating_post_canceled_text"), reply_markup=markup)
    await state.reset_state()


@dp.message_handler(TextButton("button_create_text"))
async def create_new(message: types.Message):
    markup = await cancel()
    await message.answer(text=await get_name("create_post_help_text"), reply_markup=markup)
    markup = await new_post_types_keyboard()
    await message.answer(text=await get_name("choose_type_text"), reply_markup=markup)
    await NewItem.ChooseType.set()


@dp.callback_query_handler(new_post_types_cd.filter(), state=NewItem.ChooseType)
async def choose_type(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    type_finds = callback_data.get("value")
    markup = await categories_keyboard()
    await call.message.edit_text(text=await get_name("choose_categorie_text"), reply_markup=markup)
    await NewItem.ChooseCategory.set()
    await state.update_data(type_finds=type_finds)


@dp.callback_query_handler(categories_cd.filter(value="Назад"), state=NewItem.ChooseCategory)
async def back_to_types(call: types.CallbackQuery):
    markup = await new_post_types_keyboard()
    await call.message.edit_text(text=await get_name("choose_type_text"), reply_markup=markup)
    await NewItem.ChooseType.set()


@dp.callback_query_handler(categories_cd.filter(value="Bank"), state=NewItem.ChooseCategory)
async def bank_check(call: types.CallbackQuery):
    await call.message.edit_text(await get_name("cat_bank_text"), reply_markup=BankInfoAgree.markup)


@dp.callback_query_handler(state=NewItem.ChooseCategory, text_contains="agree", admin_check=True)
async def bank_agree(call: types.CallbackQuery, state: FSMContext):
    markup = await admin_main_menu()
    await call.message.answer("Меню: ", reply_markup=markup)
    await state.reset_state()


@dp.callback_query_handler(state=NewItem.ChooseCategory, text_contains="agree")
async def bank_agree(call: types.CallbackQuery, state: FSMContext):
    markup = await main_menu()
    await call.message.answer("Меню: ", reply_markup=markup)
    await state.reset_state()


@dp.callback_query_handler(categories_cd.filter(), state=NewItem.ChooseCategory)
async def choose_category(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    category = callback_data.get("value")
    username = types.User.get_current().username
    if username:
        username_ = "@" + username
        await call.message.edit_reply_markup()
        await call.message.edit_text(text=await get_name("enter_captiob_text"))
        await NewItem.EnterCaption.set()
        await state.update_data(username=username_)

    else:
        await call.message.edit_reply_markup()
        await call.message.edit_text(
            "Юзернейм телеграм не був виявлений, вкажіть свої контакти(номер телефону, інше): ")
        await NewItem.SetContact.set()
    await state.update_data(category=category)


@dp.message_handler(state=NewItem.SetContact)
async def get_contact(message: types.Message, state: FSMContext):
    username = message.text
    await message.answer(text=await get_name("enter_captiob_text"))
    await NewItem.EnterCaption.set()
    await state.update_data(username=username)


@dp.message_handler(state=NewItem.EnterCaption, content_types=types.ContentType.TEXT)
async def enter_caption(message: types.Message, state: FSMContext):
    caption = message.text
    await message.answer(text=await get_name("ask_photo_text"), reply_markup=AskForPhotoCreatingPost.markup)
    await NewItem.AskForPhoto.set()
    await state.update_data(caption=caption)


@dp.callback_query_handler(state=NewItem.AskForPhoto, text_contains="yes")
async def send_photo(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text=await get_name("send_photo_text"))
    await NewItem.WithPhoto.set()


@dp.message_handler(state=NewItem.WithPhoto, content_types=types.ContentType.PHOTO)
async def with_photo(message: types.Message, state: FSMContext):
    user_id = int(types.User.get_current().id)
    photo = message.photo[-1].file_id
    data = await state.get_data()
    caption = data.get("caption")
    type_finds = data.get("type_finds")
    category = data.get("category")
    username = data.get("username")
    record_id = await add_new_record(photo=photo, caption=caption, type_finds=type_finds, category=category,
                                     author_username=username)
    if record_id:
        admins = await get_admins()
        if int(types.User.get_current().id) in admins:
            markup = await admin_main_menu()
            await message.answer(text=await get_name("post_success_text"), reply_markup=markup)
        else:
            markup = await main_menu()
            await message.answer(text=await get_name("post_success_text"), reply_markup=markup)
        await mailing(caption, type_finds, category, photo, username)
        await moderation(caption, type_finds, category, photo, username, record_id, user_id)
    await state.finish()


@dp.callback_query_handler(state=NewItem.AskForPhoto, text_contains="no")
async def without_photo(call: types.CallbackQuery, state: FSMContext):
    user_id = int(types.User.get_current().id)
    await call.message.delete()
    data = await state.get_data()
    caption = data.get("caption")
    type_finds = data.get("type_finds")
    category = data.get("category")
    username = data.get("username")
    record_id = await add_new_record(photo=None, caption=caption, type_finds=type_finds, category=category,
                                     author_username=username)

    if record_id:
        admins = await get_admins()
        if int(types.User.get_current().id) in admins:
            markup = await admin_main_menu()
            await call.message.answer(text=await get_name("post_success_text"), reply_markup=markup)
        else:
            markup = await main_menu()
            await call.message.answer(text=await get_name("post_success_text"), reply_markup=markup)
        await mailing(caption, type_finds, category, None, username)
        await moderation(caption, type_finds, category, None, username, record_id, user_id)
    await state.finish()
