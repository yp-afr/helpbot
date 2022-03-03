from asyncio import sleep

from aiogram import types

from findsbot.handlers.users.callbacks import change_post_cb, del_post, block_user
from findsbot.loader import bot
from findsbot.utils.dp_api.commands import get_admins, add_message


async def moderation(caption, item_type, item_category, photo, author_, post_id, user_id, record_id):
    text = f"<b>Новый пост от пользователя!</b>\n\nВ разделе {item_type} -- {item_category}\n\n"
    text += caption
    text += f"\n\nКонтакты: {author_}"
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Изменить",
                                    callback_data=change_post_cb.new(item_id=int(post_id))),
         types.InlineKeyboardButton(text="Удалить", callback_data=del_post.new(item_id=int(post_id))),
         types.InlineKeyboardButton(text="Заблокировать", callback_data=block_user.new(user_id=int(user_id)))]
    ])
    admins = await get_admins()
    for admin in admins:
        if photo:
            message: types.Message = await bot.send_photo(photo=photo, chat_id=admin, caption=text, reply_markup=markup)
            await add_message(record_id=record_id, chat_id=admin, message_id=message.message_id)
            await sleep(0.3)
        else:
            message: types.Message = await bot.send_message(chat_id=admin, text=text, reply_markup=markup)
            await add_message(record_id=record_id, chat_id=admin, message_id=message.message_id)
            await sleep(0.3)
