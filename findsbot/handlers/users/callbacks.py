import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

from findsbot.loader import dp, bot
from findsbot.states.ChangeItem import ChangeItem
from findsbot.utils.dp_api.commands import delete_record, change_record, get_name, add_user_to_block_list, \
    del_blocked_user, get_messages_by_id, delete_message_by_record_id, get_record_by_id

del_post = CallbackData("delete", "item_id")
change_post_cb = CallbackData("change", "item_id")
del_review = CallbackData("delete_review", "review_id")
block_user = CallbackData("block_user", "user_id")
del_block = CallbackData("delete_block_user", "blocked_id")


@dp.callback_query_handler(del_block.filter())
async def del_blocked(call: types.CallbackQuery, callback_data: dict):
    blocked_id = int(callback_data.get("blocked_id"))
    await del_blocked_user(blocked_id)
    chat_id = types.User.get_current().id
    msg_id = call.message.message_id
    await bot.delete_message(chat_id, msg_id)


@dp.callback_query_handler(block_user.filter())
async def block_user_func(call: types.CallbackQuery, callback_data: dict):
    try:
        user_id = int(callback_data.get("user_id"))
        await add_user_to_block_list(str(user_id))
        await call.message.answer(f"Користувач з id: {user_id} заблокований")
        chat_id = user_id
        msg = "Вас було заблоковано."
        await bot.send_message(chat_id, msg, reply_markup=None)

    except Exception as ex:
        logging.info(ex)
        await call.message.answer("Помилка блокування")


@dp.callback_query_handler(del_post.filter())
async def delete_post(call: types.CallbackQuery, callback_data: dict):
    item_id = int(callback_data.get("item_id"))
    messages = await get_messages_by_id(item_id)
    await delete_record(item_id)
    chat_id = types.User.get_current().id
    msg_id = call.message.message_id
    await bot.delete_message(chat_id, msg_id)
    if messages:
        for m in messages:
            try:
                bot.delete_message(m.chat_id, m.message_id)
            except Exception as ex:
                pass
    await delete_message_by_record_id(item_id)


@dp.callback_query_handler(change_post_cb.filter())
async def change_post(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = int(callback_data.get("item_id"))
    await call.message.reply(f"Изменение текста поста № {item_id}\n\nВведите новый текст публикации:")
    await ChangeItem.ChangeCaption.set()
    await state.update_data(item_id=item_id)


@dp.message_handler(state=ChangeItem.ChangeCaption)
async def change_caption(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get("item_id")
    try:
        await change_record(item_id, message.text)
        messages = await get_messages_by_id(item_id)
        records = await get_record_by_id(item_id)
        for record in records:
            if record.photo:
                if messages:
                    for m in messages:
                        bot.edit_message_caption(chat_id=messages.chat_id, caption=message.text)
            else:
                if messages:
                    for m in messages:
                        bot.edit_message_text(chat_id=messages.chat_id, text=message.text)

        await message.answer(text=await get_name("successful_change_text"))
    except Exception as ex:
        logging.error(ex)
    await state.reset_state()
