from asyncio import sleep

from aiogram import types

from findsbot.filters import TextButton
from findsbot.handlers.users.callbacks import change_post_cb, del_post
from findsbot.loader import dp
from findsbot.utils.dp_api.commands import load_personal_posts, get_name


@dp.message_handler(TextButton("button_myposts_text"))
async def my_posts(message: types.Message):
    rows = await load_personal_posts()
    if rows:
        for row in rows:
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Изменить", callback_data=change_post_cb.new(item_id=int(row.id))),
                 types.InlineKeyboardButton(text="Удалить", callback_data=del_post.new(item_id=int(row.id)))]
            ])
            text = "<b>" + row.type + "</b> -- " + row.category + "\n\n" + row.caption
            if row.photo is None:
                await message.answer(text, reply_markup=markup)
            else:
                await message.answer_photo(photo=row.photo, caption=text, reply_markup=markup)
            await sleep(0.3)
    else:
        await message.answer(text=await get_name("zero_presonal_posts_message"))
