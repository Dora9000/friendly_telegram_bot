from aiogram import Bot
from aiogram import F
from aiogram import Router
from aiogram.types import Message
from aiogram.types import PhotoSize
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants import GRAD_K
from bot.constants import INIT_K
from bot.constants import StatusEnum
from bot.entities.photo.manager import PhotoManager
from bot.entities.photo_to_user.manager import PhotoToUserManager
from bot.entities.user.manager import UserManager
from bot.queue.producer import GenerationProducer

router = Router()


@router.message(F.photo[-1].as_("largest_photo"))
async def download_photo(
    message: Message, bot: Bot, largest_photo: PhotoSize, session: AsyncSession
):
    user = await UserManager(session).get_or_create_user(message)

    PhotoManager(session).validator.validate_caption(message.caption)
    await PhotoToUserManager(session).validator.validate_photos_count(user_id=user.id)

    filename = await PhotoManager(session).download(bot, largest_photo)
    msg = await message.reply(f"Image saved with caption '{message.caption}'.")

    await PhotoManager(session).add_photo_for_user(
        message=msg, user_id=user.id, photo=largest_photo, prompt=message.caption
    )

    await GenerationProducer().send(
        data={
            "file_name": filename,
            "prompt": message.caption,
            "reply_chat_id": msg.chat.id,
            "grad_k": user.grad_k or GRAD_K,
            "init_k": user.init_k or INIT_K,
            "file_id": largest_photo.file_id,
            "reply_message_id": msg.message_id,
        }
    )
    await PhotoToUserManager(session).queries.update(
        values={"status": StatusEnum.RUNNING},
        filters={
            "chat_id": msg.chat.id,
            "message_id": msg.message_id,
            "status": StatusEnum.PENDING,
        },
    )
    return await bot.edit_message_text(
        text="Generation started.", chat_id=msg.chat.id, message_id=msg.message_id
    )
