from aiogram.types import PhotoSize
from sqlalchemy import insert

from bot.db import Photo
from bot.db import PhotoToUser
from bot.entities.base_manager import BaseManager
from bot.entities.photo.validator import PhotoValidator
from bot.utils import commit


class PhotoManager(BaseManager):
    model = Photo
    validator_model = PhotoValidator

    @commit
    async def add_photo_for_user(
        self, user_id: int, photo: PhotoSize, prompt: str
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

        photo_to_user = PhotoToUser(user_id=user_id, photo_id=db_photo.id)

        self._conn.add(photo_to_user)
