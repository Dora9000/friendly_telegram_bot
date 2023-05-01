from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.exceptions import DownloadErrorException
from bot.exceptions import DownloadTimeoutException
from bot.exceptions import NoCaptionException
from bot.exceptions import TooManyRequestsException


class ExceptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)

        except NoCaptionException as e:
            return await event.message.reply(e.detail)

        except TooManyRequestsException as e:
            return await event.message.reply(e.detail)

        except DownloadTimeoutException as e:
            return await event.message.reply(e.detail)

        except DownloadErrorException as e:
            return await event.message.reply(e.detail)

        except Exception as e:
            raise e
