from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from findsbot.utils.dp_api.commands import get_admins


class IsAdmin(BoundFilter):
    key = "admin_check"

    def __init__(self, admin_check):
        self.admin_check = admin_check

    async def check(self, message: types.Message) -> bool:
        list_admins = await get_admins()
        return message.from_user.id in list_admins
