import asyncio

from aiogram import Bot,  Router, F
from aiogram.exceptions import TelegramNetworkError
from aiogram.methods import SendMessage
from aiogram.types import Message, PhotoSize

from middlewares.rps import RPSMiddleware

router = Router()
# router.message.middleware(RPSMiddleware())


async def _download(photo: PhotoSize, bot: Bot) -> None:
    file = None
    while not file:
        try:
            await asyncio.wait_for(bot.download(photo, destination=f"inputs/{photo.file_id}.jpg"), timeout=3.0)
            file = True
        except asyncio.TimeoutError:
            pass


@router.message(F.photo[-1].as_("largest_photo"))
async def download_photo(message: Message, bot: Bot, largest_photo: PhotoSize):
    try:
        await asyncio.wait_for(_download(photo=largest_photo, bot=bot), timeout=15.0)
    except asyncio.TimeoutError:
        return await message.reply("Image saving timeout.")

    print(f'image {largest_photo.file_id} saved: {largest_photo.width}, {largest_photo.height}')
    return await message.reply(f"Image saved with caption '{message.caption}'.")
    # return await message.reply_photo(largest_photo.file_id, caption=f"Image saved with caption '{message.caption}'.")

