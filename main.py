import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher

from bot import settings
from bot.db.base import create_async_database
from bot.handlers.photo import router as photo_router
from bot.handlers.start import router as start_router
from bot.middlewares.exception import ExceptionMiddleware
from bot.middlewares.session import SessionMiddleware

bot = Bot(settings.BOT_TOKEN)


async def main() -> None:
    dp = Dispatcher()

    dp.include_routers(photo_router, start_router)

    async_session = await create_async_database()

    dp.update.middleware(SessionMiddleware(session_pool=async_session))
    dp.update.middleware(ExceptionMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
