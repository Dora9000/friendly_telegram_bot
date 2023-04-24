import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher

import settings
from db.base import create_async_database
from handlers.photo import router as image_router
from handlers.start import router as start_router
from middlewares.session import SessionMiddleware

bot = Bot(settings.BOT_TOKEN)


async def main() -> None:
    dp = Dispatcher()

    dp.include_routers(image_router, start_router)

    async_session = await create_async_database()

    dp.update.middleware(SessionMiddleware(session_pool=async_session))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
