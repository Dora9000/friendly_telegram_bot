import asyncio
import logging

from aiogram import Bot
from aiogram.types import Message
from aiogram.types import PhotoSize
from sqlalchemy import insert

from bot.db import Photo
from bot.db import PhotoToUser
from bot.entities.base_manager import BaseManager
from bot.entities.photo.validator import PhotoValidator
from bot.exceptions import DownloadErrorException
from bot.exceptions import DownloadTimeoutException
from bot.utils import commit
from bot.utils import upload_to_server


class PhotoManager(BaseManager):
    model = Photo
    validator_model = PhotoValidator

    @commit
    async def add_photo_for_user(
        self, message: Message, user_id: int, photo: PhotoSize, prompt: str
    ) -> None:
        # TODO: check how many files already exist
        photo = Photo(
            prompt=prompt,
            file_id=photo.file_id,
            height=photo.height,
            width=photo.width,
            file_size=photo.file_size,
            file_unique_id=photo.file_unique_id,
        )
        db_photo = await self._conn.execute(
            insert(Photo)
            .values(
                prompt=prompt,
                file_id=photo.file_id,
                height=photo.height,
                width=photo.width,
                file_size=photo.file_size,
                file_unique_id=photo.file_unique_id,
            )
            .returning(Photo)
        )
        db_photo = db_photo.scalar()

        photo_to_user = PhotoToUser(
            user_id=user_id,
            photo_id=db_photo.id,
            chat_id=message.chat.id,
            message_id=message.message_id,
        )

        self._conn.add(photo_to_user)

    async def _download(self, photo: PhotoSize, bot: Bot) -> None:
        is_uploaded = False
        while not is_uploaded:
            try:
                await asyncio.wait_for(
                    bot.download(
                        photo,
                        destination=f"inputs/{self.get_input_filename(photo.file_id)}",
                    ),
                    timeout=3.0,
                )
                upload_to_server(input_filename=self.get_input_filename(photo.file_id))
                is_uploaded = True
            except asyncio.TimeoutError:
                pass

    @staticmethod
    def get_input_filename(file_id: str) -> str:
        return f"{file_id}.jpg"

    async def download(self, bot: Bot, photo: PhotoSize) -> str:
        try:
            await asyncio.wait_for(self._download(photo=photo, bot=bot), timeout=15.0)

        except asyncio.TimeoutError:
            raise DownloadTimeoutException()

        except Exception as e:
            logging.error(e, e.__str__())
            raise DownloadErrorException()

        logging.info(f"image {photo.file_id} saved: {photo.width}, {photo.height}")

        return self.get_input_filename(photo.file_id)
