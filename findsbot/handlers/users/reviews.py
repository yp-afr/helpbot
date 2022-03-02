import asyncio

from aiogram import types

from findsbot.filters import TextButton
from findsbot.handlers.users.callbacks import del_review
from findsbot.loader import dp, bot
from findsbot.utils.dp_api.commands import get_reviews, delete_review


@dp.message_handler(TextButton("button_show_reviews"), admin_check=True)
async def list_reviews(message: types.Message):
    rows = await get_reviews()
    if rows:
        for row in rows:
            text = str(row.caption) + "\n\n"
            text += f"<a href='tg://user?id={row.author_id}'>Автор отзыва</a>"
            markup = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Удалить", callback_data=del_review.new(review_id=row.id))]
            ])
            await message.answer(text, reply_markup=markup)
            await asyncio.sleep(0.3)
    else:
        await message.answer("Пусто!")


@dp.callback_query_handler(del_review.filter())
async def delete_post(call: types.CallbackQuery, callback_data: dict):
    review_id = int(callback_data.get("review_id"))
    await delete_review(review_id)
    chat_id = types.User.get_current().id
    msg_id = call.message.message_id
    await bot.delete_message(chat_id, msg_id)
