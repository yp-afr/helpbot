from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from findsbot.utils.dp_api.commands import get_blocked_users


class IsBlocked(BoundFilter):
    key = "block_check"

    def __init__(self, block_check):
        self.block_check = block_check

    async def check(self, message: types.Message) -> bool:
        list_blocked = await get_blocked_users()
        return int(message.from_user.id) in list_blocked
