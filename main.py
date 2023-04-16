import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types, F
from handlers.photo import router as image_router
from handlers.start import router as start_router
import settings


bot = Bot(settings.BOT_TOKEN, parse_mode="HTML")


async def main() -> None:
    dp = Dispatcher()

    dp.include_routers(image_router, start_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
