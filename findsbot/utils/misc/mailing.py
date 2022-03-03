from asyncio import sleep

from aiogram import types

from findsbot.loader import bot
from findsbot.utils.dp_api.commands import get_users, get_all_contacts, add_message


async def mailing(caption, item_type, item_category, photo, author_, record_id):
    type_ = item_type
    if type_ == "Потребують допомоги":
        type_ = "Нададуть допомогу"
    elif type_ == "Нададуть допомогу":
        type_ = "Потребують допомоги"
    results = await get_users(type_, item_category)
    for result in results:
        text = f"<b>Нове оголошення яке відноситься до твоєї категорії!\n\n" \
               f"</b><b>{item_type}</b> -- {item_category}\n\n"
        contacts = await get_all_contacts()
        for contact in contacts:
            if str(author_) == str(contact.name):
                author_ += "\n\n<i><b>Перевірений користувач</b></i>"
                break

        try:
            if photo:
                text += caption
                text += f"\n\nКонтакти: {author_}"
                message: types.Message = await bot.send_photo(photo=photo, chat_id=result.author_id, caption=text)
                await add_message(record_id=record_id, chat_id=result.author_id, message_id=message.message_id)
                await sleep(0.3)
            else:
                text += caption
                text += f"\n\nКонтакти: {author_}"
                message: types.Message = await bot.send_message(chat_id=result.author_id, text=text)
                await add_message(record_id=record_id, chat_id=result.author_id, message_id=message.message_id)
                await sleep(0.3)
        except Exception:
            pass
