from bot.entities.base_validator import BaseValidator
from bot.exceptions import TooManyRequestsException
from bot.settings import MAX_REQUESTS


class PhotoToUserValidator(BaseValidator):
    async def validate_photos_count(self, user_id: int) -> None:
        if (
            await self.queries.get_count(
                filters={"user_id": user_id, "status": "pending"}
            )
            > MAX_REQUESTS
        ):
            raise TooManyRequestsException()
