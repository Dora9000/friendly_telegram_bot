from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.exceptions import NoCaptionException


class ExceptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        try:
            await handler(event, data)

        except NoCaptionException as e:
            return event.message.reply(e.detail)

        except Exception as e:
            raise e
