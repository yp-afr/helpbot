import logging
from typing import List

from aiogram import types
from sqlalchemy import and_

from findsbot.utils.dp_api.schemas.admins import Admins
from findsbot.utils.dp_api.schemas.blocklist import Block
from findsbot.utils.dp_api.schemas.contacts import Contact
from findsbot.utils.dp_api.schemas.info import Info
from findsbot.utils.dp_api.schemas.names import Names
from findsbot.utils.dp_api.schemas.records import Records
from findsbot.utils.dp_api.schemas.records_users import RecordsUsers
from findsbot.utils.dp_api.schemas.reviews import Reviews
from findsbot.utils.dp_api.schemas.users import User


async def add_user(user_id: int):
    try:
        user = User(user_id=user_id)
        await user.create()
    except Exception as ex:
        logging.info(ex)


async def add_contactt(contact: str):
    try:
        contact = Contact(name=contact)
        await contact.create()
    except Exception as ex:
        logging.info(ex)


async def add_new_review(caption):
    try:
        author_id = types.User.get_current().id
        review = Reviews(author_id=author_id, caption=caption)
        await review.create()
    except Exception as ex:
        logging.error(ex)


async def delete_review(review_id):
    try:
        await Reviews.delete.where(Reviews.id == review_id).gino.status()
    except Exception as ex:
        logging.error(ex)


async def get_reviews():
    try:
        return await Reviews.query.gino.all()
    except Exception as ex:
        logging.error(ex)


async def delete_contact(contact_id):
    try:
        await Contact.delete.where(Contact.id == int(contact_id)).gino.status()
    except Exception as ex:
        logging.error(ex)


async def get_all_contacts():
    try:
        return await Contact.query.gino.all()
    except Exception as ex:
        logging.error(ex)


async def add_user_to_block_list(user_id: str):
    try:
        block = Block(name=user_id)
        await block.create()
    except Exception as ex:
        logging.info(ex)


async def del_blocked_user(blocked_id):
    try:
        await Block.delete.where(Block.id == int(blocked_id)).gino.status()
    except Exception as ex:
        logging.error(ex)


async def get_blocked():
    try:
        return await Block.query.gino.all()
    except Exception as ex:
        logging.error(ex)


async def get_blocked_users() -> list:
    try:
        blocks = await Block.query.gino.all()
        ids = []
        for b in blocks:
            ids.append(int(b.name))
        return ids
    except Exception as ex:
        logging.error(ex)


async def add_iinfo(info: str):
    try:
        info = Info(name=info)
        await info.create()
    except Exception as ex:
        logging.info(ex)


async def get_info():
    try:
        return await Info.query.gino.all()
    except Exception as ex:
        logging.error(ex)


async def delete_info(info_id):
    try:
        await Info.delete.where(Info.id == int(info_id)).gino.status()
    except Exception as ex:
        logging.error(ex)


async def add_new_record(photo, caption, type_finds, category, author_username):
    try:
        author_id = types.User.get_current().id
        record = Records(author_id=author_id, author_username=author_username, photo=photo, caption=caption,
                         type=type_finds, category=category)
        record_created = await record.create()
        return record_created.id
    except Exception as ex:
        logging.error(ex)


async def load_personal_posts():
    try:
        author_id = types.User.get_current().id
        records = await Records.query.where(Records.author_id == author_id).gino.all()
        return records
    except Exception as ex:
        logging.error(ex)


async def delete_record(record_id):
    try:
        await Records.delete.where(Records.id == record_id).gino.status()
    except Exception as ex:
        logging.error(ex)


async def change_record(record_id, caption):
    try:
        await Records.update.values(caption=caption).where(Records.id == record_id).gino.first()
    except Exception as ex:
        logging.error(ex)


async def get_records(type_finds, category):
    try:
        return await Records.query.where(and_(Records.type == type_finds, Records.category == category)).gino.all()
    except Exception as ex:
        logging.error(ex)


async def get_users(type_finds, category):
    try:
        return await Records.query.where(and_(Records.type == type_finds, Records.category == category)).gino.all()
    except Exception as ex:
        logging.error(ex)


async def get_admins() -> List:
    try:
        admins = await Admins.query.gino.all()
        ids = []
        for admin in admins:
            ids.append(int(admin.admin_id))
        return ids
    except Exception as ex:
        logging.info(ex)


async def get_name(name_code):
    try:
        name: Names = await Names.query.where(Names.name == name_code).gino.first()
        return name.value
    except Exception as ex:
        logging.info(ex)


async def get_all_admins():
    try:
        admins = await Admins.query.gino.all()
        return admins
    except Exception as ex:
        logging.info(ex)


async def add_admin(phone, first_name, admin_id: str):
    admin = Admins(phone_number=phone, first_name=first_name, admin_id=admin_id)
    await admin.create()


async def del_admin(phone):
    try:
        await Admins.delete.where(Admins.phone_number == phone).gino.status()
    except Exception as ex:
        logging.info(ex)


async def get_all_users() -> List:
    try:
        users = await User.query.gino.all()
        ids = []
        for user in users:
            ids.append(user.user_id)
        return ids
    except Exception as ex:
        logging.info(ex)


async def add_message(record_id: int, chat_id: int, message_id: int):
    try:
        record = RecordsUsers(record_id=record_id, chat_id=chat_id, message_id=message_id)
        record_created = await record.create()
        return record_created.id
    except Exception as ex:
        logging.error(ex)


async def get_messages_by_id(record_id):
    try:
        return await RecordsUsers.query.where(RecordsUsers.record_id == record_id).gino.all()
    except Exception as ex:
        logging.error(ex)


async def get_records_by_author(id):
    try:
        return await Records.query.where(Records.author_id == id).gino.all()
    except Exception as ex:
        logging.error(ex)

async def get_record_by_id(id):
    try:
        return await Records.query.where(Records.id == id).gino.all()
    except Exception as ex:
        logging.error(ex)


async def delete_message_by_record_id(id: int):
    try:
        await RecordsUsers.delete.where(RecordsUsers.record_id == id).gino.status()
    except Exception as ex:
        logging.info(ex)
