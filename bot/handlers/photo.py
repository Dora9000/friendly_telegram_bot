import asyncio
import logging

from aiogram import Bot
from aiogram import F
from aiogram import Router
from aiogram.types import Message
from aiogram.types import PhotoSize
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User
from bot.entities.photo.manager import PhotoManager
from bot.entities.user.manager import UserManager

router = Router()


async def _download(photo: PhotoSize, bot: Bot) -> None:
    file = None
    while not file:
        try:
            await asyncio.wait_for(
                bot.download(photo, destination=f"inputs/{photo.file_id}.jpg"),
                timeout=3.0,
            )
            file = True
        except asyncio.TimeoutError:
            pass


@router.message(F.photo[-1].as_("largest_photo"))
async def download_photo(
    message: Message,
    bot: Bot,
    largest_photo: PhotoSize,
    session: AsyncSession,
    **kwargs,
):
    user = await UserManager(session).get_entity(filters={"id": message.from_user.id})

    if not user or True:
        user = await UserManager(session).create(
            entity=User(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                username=message.from_user.username,
            )
        )

    try:
        await asyncio.wait_for(_download(photo=largest_photo, bot=bot), timeout=15.0)
    except asyncio.TimeoutError:
        return await message.reply("Image saving timeout.")

    logging.info(
        f"image {largest_photo.file_id} saved: {largest_photo.width}, {largest_photo.height}"
    )

    PhotoManager(session).validator.validate_caption(message.caption)

    await PhotoManager(session).add_photo_for_user(
        user_id=user.id, photo=largest_photo, prompt=message.caption
    )

    return await message.reply(f"Image saved with caption '{message.caption}'.")
