import datetime
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class RPSMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self._last_request = {}
        self._blocked = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        now = datetime.datetime.utcnow()
        user_id = event.from_user.id

        #  TODO: lock by user_id

        if event.photo:  # or event.document
            last_timestamp = self._last_request.get(user_id)
            self._last_request[user_id] = now

            if last_timestamp and (now - last_timestamp).total_seconds() < 5:
                if not self._blocked.get(user_id):
                    await event.reply("Too many requests!", show_alert=True)
                self._blocked[user_id] = True

                return

            else:
                self._blocked[user_id] = False

        return await handler(event, data)
