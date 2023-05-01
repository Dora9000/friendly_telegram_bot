import asyncio

from aiogram import Bot
from aiogram.types import FSInputFile

from bot.constants import StatusEnum
from bot.entities.photo_to_user.manager import PhotoToUserManager
from bot.utils import download_from_server


class StatusConsumer:
    @staticmethod
    async def _send(f, **kwargs) -> None:
        is_done = False
        while not is_done:
            try:
                await asyncio.wait_for(f(**kwargs), timeout=3.0)
                is_done = True
            except asyncio.TimeoutError:
                pass

    @classmethod
    async def react_message(cls, message: dict, async_session, bot: Bot) -> None:
        # generation_message_id = message["generation_message_id"]
        percent = message["percent"]
        file_name = message.get("file_name")

        chat_id = message["reply_chat_id"]
        message_id = message["reply_message_id"]

        await cls._send(
            f=bot.edit_message_text,
            text=f"Generated on {percent}%",
            chat_id=message["reply_chat_id"],
            message_id=message["reply_message_id"],
        )

        if file_name:
            file_path = download_from_server(output_filename=file_name)

            async with async_session() as session:
                await PhotoToUserManager(session).queries.update(
                    filters={
                        "chat_id": chat_id,
                        "message_id": message_id,
                        "status": StatusEnum.RUNNING,
                    },
                    values={"status": StatusEnum.DONE, "result_photo_name": file_name},
                )

            photo = FSInputFile(file_path)
            await bot.send_photo(
                caption="Generation finished!",
                chat_id=chat_id,
                photo=photo,
                reply_to_message_id=message_id,
            )
